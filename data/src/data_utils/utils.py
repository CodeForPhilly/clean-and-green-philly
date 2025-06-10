import os

import requests


def save_stream_url(url: str) -> str:
    """download the file from this url to the tmp/ directory by streaming in a memory-friendly way.
    If local file already exists, use it and don't download.
    Args:
        url (str): the url of the zip file

    Returns:
        str: the relative local path of the saved zip file
    """
    local_filename = "tmp/" + url.split("/")[-1]
    if os.path.exists(local_filename):
        return local_filename

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
            f.close()
        r.close()
    return local_filename
