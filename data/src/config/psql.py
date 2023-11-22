import os
from sqlalchemy import create_engine
from config.config import USE_LOCAL_DB, USE_REMOTE_DB

connections = []

# Connect to local psql
if USE_LOCAL_DB:
    local_engine = create_engine(os.environ["VACANT_LOTS_DB"].replace(
        "localhost", "docker.host.internal"))
    local_conn = local_engine.connect()
    connections.append(local_conn)


# Connect to remote psql
if USE_REMOTE_DB:
    remote_engine = create_engine(os.environ["VACANT_LOTS_DB_REMOTE"])
    remote_conn = remote_engine.connect()
    connections.append(remote_conn)
