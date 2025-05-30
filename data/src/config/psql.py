import os

from sqlalchemy import create_engine

from src.config.config import is_docker

url: str = (
    os.environ["VACANT_LOTS_DB"].replace("localhost", "host.docker.internal")
    if is_docker()
    else os.environ["VACANT_LOTS_DB"]
)
local_engine = create_engine(url)
conn = local_engine.connect()
