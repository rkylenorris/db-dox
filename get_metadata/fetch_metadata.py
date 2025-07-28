import os
import pyodbc
import pandas as pd

QUERIES_DIR = os.path.join(os.path.dirname(__file__), 'queries')

# List of SQL files to run
QUERY_FILES = [
    'get_functions.sql',
    'get_procs.sql',
    'get_sp_params.sql',
    'get_views.sql',
    'references.sql',
]

def get_connection(server, database, user, password, driver="ODBC Driver 17 for SQL Server"):
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password}"
    )
    return pyodbc.connect(conn_str)

def run_query_from_file(conn, sql_file):
    with open(os.path.join(QUERIES_DIR, sql_file), 'r', encoding='utf-8') as f:
        sql = f.read()
    return pd.read_sql(sql, conn)

def fetch_all_metadata(conn):
    results = {}
    for qf in QUERY_FILES:
        try:
            df = run_query_from_file(conn, qf)
            results[qf.replace('.sql', '')] = df
        except Exception as e:
            results[qf.replace('.sql', '')] = f"Error: {e}"
    return results

if __name__ == "__main__":
    # Example usage: fill in your connection details
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_NAME', 'master')
    user = os.getenv('DB_USER', 'sa')
    password = os.getenv('DB_PASSWORD', 'your_password')

    conn = get_connection(server, database, user, password)
    metadata = fetch_all_metadata(conn)
    for key, value in metadata.items():
        print(f"\n--- {key} ---")
        print(value)
