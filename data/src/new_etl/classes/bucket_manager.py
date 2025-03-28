import logging as log
import os

from google.cloud import storage

from config.config import log_level

log.basicConfig(level=log_level)


class GCSBucketManager:
    """
    A manager for interacting with a Google Cloud Storage bucket.

    This class initializes a bucket client using Application Default Credentials,
    an optional service account key, or falls back to an anonymous client for read-only access.
    """

    def __init__(
        self, bucket_name: str = None, credential_path: str = None, client=None
    ):
        """
        Initialize the GCSBucketManager.

        Args:
            bucket_name (str): Name of the bucket. Defaults to the environment variable
                               'GOOGLE_CLOUD_BUCKET_NAME' or "cleanandgreenphl" if not set.
            credential_path (str): Optional path to a service account credentials file.
            client: Optional storage. Client instance for dependency injection in testing.
        """
        self.bucket_name = bucket_name or os.getenv(
            "GOOGLE_CLOUD_BUCKET_NAME", "cleanandgreenphl"
        )

        self.read_only = False

        if client is not None:
            self._client = client
        else:
            self._client = self._init_client(credential_path)

        self.bucket = self._client.bucket(self.bucket_name)

    def _init_client(self, credential_path: str = None):
        """
        Attempt to initialize the storage client using a credential file, application default
        credentials or fall back to anonymous/read-only.
        """
        project_name = os.getenv("GOOGLE_CLOUD_PROJECT", "clean-and-green-philly")
        credentials_path = credential_path or "/app/service-account-key.json"

        if os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        try:
            # This will use application default credentials if GOOGLE_APPLICATION_CREDENTIALS is not set
            return storage.Client(project=project_name)

        except Exception as e:
            log.warning(f"Failed to initialize client with service account key: {e}")
            log.warning("Falling back to anonymous client (read-only mode)")
            self.read_only = True
            return storage.Client.create_anonymous_client()
