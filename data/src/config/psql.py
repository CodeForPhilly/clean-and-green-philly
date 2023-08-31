import os
from sqlalchemy import create_engine

# Connect to psql
engine = create_engine(os.environ["VACANT_LOTS_DB"])
conn = engine.connect()
