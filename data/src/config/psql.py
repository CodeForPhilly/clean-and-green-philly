import os
from sqlalchemy import create_engine

# Connect to local psql
local_engine = create_engine(os.environ["VACANT_LOTS_DB"])
local_conn = local_engine.connect()


# Connect to remote psql
remote_engine = create_engine(os.environ["VACANT_LOTS_DB_REMOTE"])
remote_conn = remote_engine.connect()