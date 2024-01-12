import os
from sqlalchemy import create_engine

local_engine = create_engine(
    os.environ["VACANT_LOTS_DB"].replace("localhost", "host.docker.internal")
)
conn = local_engine.connect()
