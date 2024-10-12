import concurrent.futures
import os
import time
from urllib.parse import quote

import pandas as pd
import requests
from classes.featurelayer import google_cloud_bucket
from config.psql import conn
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

# Configure Google
bucket = google_cloud_bucket()
key = os.environ["CLEAN_GREEN_GOOGLE_KEY"]
bucket_name = bucket.name

# Configure requests session with retries and connection pooling
session = requests.Session()
retry_strategy = Retry(
    total=0,  # Number of retries
    backoff_factor=1,  # Exponential backoff: 1 second, 2 seconds, etc.
    status_forcelist=[500, 502, 503, 504],  # Retry for these status codes
)
adapter = HTTPAdapter(
    max_retries=retry_strategy, pool_connections=200, pool_maxsize=200
)
session.mount("http://", adapter)
session.mount("https://", adapter)

failed_addresses = []


# Helper Functions
def get_streetview_metadata(address):
    url = f"http://example.com/metadata/{address}"
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        # Silently handle the failure by appending the address to the failed list
        failed_addresses.append(address)
        return None


def get_streetview_image(address):
    """Fetches an image from the Street View API."""
    image_url = f"https://maps.googleapis.com/maps/api/streetview?location={quote(address)}, Philadelphia, PA&key={key}&size=600x400"
    response = session.get(image_url)
    return response.content


def upload_image_with_metadata(blob, image_content, metadata, address):
    """Uploads an image with metadata to a GCP bucket."""
    blob.metadata = metadata
    blob.upload_from_string(image_content, content_type="image/jpeg")


# Load Data
properties = pd.read_sql("select * from vacant_properties_end", conn)
print(len(properties), "properties loaded from database")

# Get list of all filenames in bucket
blobs = bucket.list_blobs(prefix="streetview_images/")
blobs = [blob.name.split("/")[-1].split(".")[0] for blob in blobs]
print(f"Found {len(blobs)} images in the streetview_images/ subdirectory")

# Remove from properties any value of opa_id that is in blobs
properties = properties[~properties.opa_id.astype(str).isin(blobs)]
print(f"Found {len(properties)} images to fetch")


def process_row(row):
    opa_id = row["opa_id"]
    file_name = f"{opa_id}.jpg"
    blob = bucket.blob(file_name)

    # Check if file already exists
    if not blob.exists():
        try:
            # Fetch image and metadata, then upload
            image_content = get_streetview_image(row["address"])
            metadata = get_streetview_metadata(row["address"])
            if metadata:
                upload_image_with_metadata(
                    blob, image_content, metadata, row["address"]
                )
        except Exception as e:
            print(f"Error processing {row['address']}: {e}")

    time.sleep(0.5)


# Function to retry failed addresses until all succeed
def retry_failed_addresses():
    while failed_addresses:
        print(f"Retrying {len(failed_addresses)} failed addresses...")
        failed = failed_addresses.copy()  # Make a copy to iterate over
        failed_addresses.clear()  # Clear the list to track new failures

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(
                tqdm(
                    executor.map(
                        process_row,
                        [{"opa_id": None, "address": addr} for addr in failed],
                    ),
                    total=len(failed),
                )
            )


# Retry failed addresses sequentially until
def process_failed_addresses_sequentially():
    if failed_addresses:
        print(f"Retrying {len(failed_addresses)} failed addresses sequentially...")

        for address in tqdm(failed_addresses, desc="Retrying failed addresses"):
            # Simulate the original logic for failed addresses
            file_name = f"streetview_images/{address}.jpg"
            blob = bucket.blob(file_name)

            # Check if the image already exists
            if blob.exists():
                print(f"Image {file_name} already exists")
            else:
                # Fetch image and metadata, then upload
                print(f"Fetching image for {address}")
                image_content = get_streetview_image(address)
                metadata = get_streetview_metadata(address)
                if metadata:
                    upload_image_with_metadata(blob, image_content, metadata)
                    print(f"Successfully uploaded image for {address}")

            # Add a slight delay between retries to avoid overwhelming the server
            time.sleep(0.5)

        print("All failed addresses have been processed.")


# Parallelize the operation with progress tracking
max_workers = os.cpu_count() // 2  # Dynamically set max workers
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    list(
        tqdm(
            executor.map(process_row, [row for _, row in properties.iterrows()]),
            total=len(properties),
        )
    )


process_failed_addresses_sequentially()
