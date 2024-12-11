from sqlalchemy import text


def is_hypertable(conn, table_name):
    """
    Check if a given table is already a hypertable.

    Args:
        conn: SQLAlchemy connection to the database.
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table is a hypertable, False otherwise.
    """
    query = f"""
    SELECT EXISTS (
        SELECT 1
        FROM timescaledb_information.hypertables
        WHERE hypertable_name = '{table_name}'
    );
    """
    result = conn.execute(text(query)).scalar()
    return result


def execute_optional_sql(conn, query, description):
    """
    Execute a SQL query in a separate transaction and handle errors gracefully.

    Args:
        conn: SQLAlchemy connection to the database.
        query (str): The SQL query to execute.
        description (str): A description of the operation for logging purposes.
    """
    try:
        conn.execute(text(query))
    except Exception as e:
        print(f"Warning: {description} failed. Error: {e}")


def sync_table_schema(gdf, table_name, conn):
    """
    Synchronize the schema of a GeoDataFrame with the database table.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame with updated schema.
        table_name (str): The name of the table in the database.
        conn: SQLAlchemy connection to the database.
    """
    result = conn.execute(
        text(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}';
        """)
    )
    existing_columns = {row[0] for row in result}
    for column in set(gdf.columns) - existing_columns:
        dtype = gdf[column].dtype
        sql_type = {
            "int64": "INTEGER",
            "float64": "FLOAT",
            "object": "TEXT",
            "bool": "BOOLEAN",
            "datetime64[ns]": "TIMESTAMP",
        }.get(str(dtype), "TEXT")
        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column} {sql_type};"))


def to_postgis_with_schema(gdf, table_name, conn, if_exists="append", chunksize=1000):
    """
    Save a GeoDataFrame to PostGIS, ensure the `create_date` column exists, and configure the table as a hypertable.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame to save.
        table_name (str): The name of the table in PostGIS.
        conn: SQLAlchemy connection to the database.
        if_exists (str): Behavior when the table already exists ('replace', 'append', 'fail').
        chunksize (int): Number of rows to write at a time.
    """
    try:
        # Begin a transaction
        with conn.begin() as transaction:
            # Synchronize schema with database table
            if if_exists == "append":
                sync_table_schema(gdf, table_name, conn)

            # Save GeoDataFrame to PostGIS
            gdf.to_postgis(table_name, conn, if_exists=if_exists, chunksize=chunksize)

            # Add the `create_date` column via SQL
            conn.execute(
                text(f"""
                DO $$
                BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}' AND column_name = 'create_date'
                ) THEN
                    ALTER TABLE {table_name} ADD COLUMN create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                END $$;
                """)
            )

            # Check if the table is already a hypertable
            if not is_hypertable(conn, table_name):
                conn.execute(
                    text(f"""
                    SELECT create_hypertable('{table_name}', 'create_date', migrate_data => true);
                    """)
                )

            # Optional operations in separate transactions
            execute_optional_sql(
                conn,
                f"SELECT set_chunk_time_interval('{table_name}', INTERVAL '1 month');",
                f"Setting chunk interval for {table_name}",
            )
            execute_optional_sql(
                conn,
                f"ALTER TABLE {table_name} SET (timescaledb.compress);",
                f"Enabling compression on {table_name}",
            )
            execute_optional_sql(
                conn,
                f"SELECT add_compression_policy('{table_name}', INTERVAL '3 months', if_not_exists => true);",
                f"Adding compression policy for {table_name}",
            )
    except Exception as e:
        # Rollback the transaction on any error
        conn.rollback()
        raise RuntimeError(f"Error during to_postgis_with_schema: {e}")
