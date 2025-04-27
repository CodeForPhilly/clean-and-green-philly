import os

from sqlalchemy import create_engine

from config.config import is_docker


def get_db_url():
    # Detect if running in Cloud Run:
    is_cloud_run = "K_SERVICE" in os.environ or "CLOUD_RUN_JOB" in os.environ

    # Use host.docker.internal when running locally in Docker
    # except when running in Cloud Run
    host = "localhost"
    if is_docker() and not is_cloud_run:
        host = "host.docker.internal"

    if os.getenv("VACANT_LOTS_DB"):
        # Use the provided database URL
        url = os.getenv("VACANT_LOTS_DB")
        url = url.replace("localhost", host)
    else:
        # Use the specified port, pw, db and user to construct the URL
        pw = os.environ["POSTGRES_PASSWORD"]
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "vacantlotdb")
        user = os.getenv("POSTGRES_USER", "postgres")
        url: str = f"postgresql://{user}:{pw}@{host}:{port}/{db}"
        print(f"Set database url to: postgresql://{user}:****@{host}:{port}/{db}")
    return url


url = get_db_url()

local_engine = create_engine(url)
conn = local_engine.connect()
