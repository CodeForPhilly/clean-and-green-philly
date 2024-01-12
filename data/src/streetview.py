import os
import requests
from urllib.parse import quote
from google.cloud import storage
import pandas as pd
from config.psql import conn
import time


# Configure Google
key = os.environ['CLEAN_GREEN_GOOGLE_KEY']
credentials_path = os.path.expanduser(
    '~/.config/gcloud/application_default_credentials.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
bucket_name = 'cleanandgreenphilly'
storage_client = storage.Client(project='helpful-graph-407400')
bucket = storage_client.bucket(bucket_name)


# Load Data
properties = pd.read_sql('select * from vacant_properties_end', conn)

# Get list of all filenames in bucket
blobs = bucket.list_blobs()
blobs = [blob.name.split('.')[0] for blob in blobs]
print(f"Found {len(blobs)} images in bucket")

# Remove from properties any value of OPA_ID that is in blobs
properties = properties[~properties.OPA_ID.astype(str).isin(blobs)]


for idx, row in properties.iterrows():
    opa_id = row['OPA_ID']
    file_name = f'{opa_id}.jpg'

    # check if file already exists
    if bucket.blob(file_name).exists():
        print(f"Image {file_name} already exists")
        continue

    address = quote(f'{row["address"]}, Philadelphia, PA')
    url = f'https://maps.googleapis.com/maps/api/streetview?location={address}&key={key}&size=600x400'

    r = requests.get(url)

    if r.status_code == 200:
        # Create a blob and upload the image content
        blob = bucket.blob(file_name)
        blob.upload_from_string(r.content, content_type='image/jpeg')
        print(f"Image uploaded to {bucket_name}/{file_name}")
    else:
        print(f"Error: {r.status_code}")
