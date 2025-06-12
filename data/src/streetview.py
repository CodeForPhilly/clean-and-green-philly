import os
import time
from urllib.parse import quote

import pandas as pd
import requests

from src.classes.loaders import google_cloud_bucket
from src.config.psql import conn

# Configure Google
bucket = google_cloud_bucket()
# when switching over to new_etl, this will need to be updated to use the new bucket manager
# bucket = google_cloud_bucket(require_write_access=True)
# if bucket is None:
#   do a dry run or exit
key = os.environ["CLEAN_GREEN_GOOGLE_KEY"]
bucket_name = bucket.name


# Helper Functions
def get_streetview_metadata(address):
    """Fetches metadata from the Street View API."""
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={quote(address)}, Philadelphia, PA&key={key}"
    response = requests.get(url)
    return response.json()


def get_streetview_image(address):
    """Fetches an image from the Street View API."""
    image_url = f"https://maps.googleapis.com/maps/api/streetview?location={quote(address)}, Philadelphia, PA&key={key}&size=600x400"
    response = requests.get(image_url)
    return response.content


def update_blob_metadata(blob, metadata):
    """Updates the metadata of an existing blob."""
    blob.metadata = metadata
    blob.patch()
    print(f"Metadata updated for {blob.name}")


def upload_image_with_metadata(blob, image_content, metadata):
    """Uploads an image with metadata to a GCP bucket."""
    blob.metadata = metadata
    blob.upload_from_string(image_content, content_type="image/jpeg")
    print(f"Image uploaded to {bucket_name}/{blob.name} with metadata")


# Load Data
properties = pd.read_sql("select * from vacant_properties_end", conn)
print(len(properties), "properties loaded from database")

# Get list of all filenames in bucket
blobs = bucket.list_blobs()
blobs = [blob.name.split(".")[0] for blob in blobs]
print(f"Found {len(blobs)} images in bucket")

# Remove from properties any value of opa_id that is in blobs
properties = properties[~properties.opa_id.astype(str).isin(blobs)]
print(f"Found {len(properties)} images to fetch")


for idx, row in properties.iterrows():
    opa_id = row["opa_id"]
    file_name = f"{opa_id}.jpg"
    blob = bucket.blob(file_name)

    # Check if file already exists (shouldn't happen based on above code, but just to confirm)
    if blob.exists():
        print(f"Image {file_name} already exists")

    else:
        # Get streetview image
        print(f"Fetching image for {row['address']}")
        image_content = get_streetview_image(row["address"])
        metadata = get_streetview_metadata(row["address"])
        upload_image_with_metadata(blob, image_content, metadata)

    time.sleep(0.5)
