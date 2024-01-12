import os
from sqlalchemy import create_engine

local_engine = create_engine(
    # .replace("localhost", "host.docker.internal")
    os.environ["VACANT_LOTS_DB"]
)
conn = local_engine.connect()
