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
        try:
            conn.execute(
                text(f"""
                SELECT create_hypertable('{table_name}', 'create_date', migrate_data => true);
                """)
            )
        except Exception as e:
            print(
                f"Warning: Failed to convert {table_name} to a hypertable. Error: {e}"
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
        f"SELECT add_compression_policy('{table_name}', INTERVAL '3 months');",
        f"Adding compression policy for {table_name}",
    )
