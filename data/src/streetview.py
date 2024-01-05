import os
import requests
from urllib.parse import quote
from google.cloud import storage
import pandas as pd
from config.psql import connections


# Configure Google
key = os.environ['CLEAN_GREEN_GOOGLE_KEY']
credentials_path = os.path.expanduser(
    '~/.config/gcloud/application_default_credentials.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
bucket_name = 'cleanandgreenphilly'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)


# Load Data
conn = connections[0]
properties = pd.read_sql('select * from vacant_properties_end', conn).head(5)


for idx, row in properties.iterrows():
    file_name = f'{row["parcel_number"]}.jpg'

    address = f'{quote(row["address"])}, Philadelphia, PA'
    url = f'https://maps.googleapis.com/maps/api/streetview?location={address}&key={key}&size=600x400'

    r = requests.get(url)

    if r.status_code == 200:
        # Create a blob and upload the image content
        blob = bucket.blob(file_name)
        blob.upload_from_string(r.content, content_type='image/jpeg')
        print(f"Image uploaded to {bucket_name}/{file_name}")
    else:
        print(f"Error: {r.status_code}")
