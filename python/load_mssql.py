import urllib
import pandas as pd
from sqlalchemy import create_engine, text

# Database Connection Settings
SERVER = 'localhost'  # or r'localhost\SQLEXPRESS'
DATABASE = 'FlowMetrics'

# ODBC Connection String for SQL Server
CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

params = urllib.parse.quote_plus(CONNECTION_STRING)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)


def load_table(connection, csv_path, table_name):
    print(f"Loading {table_name} from {csv_path}...")
    df = pd.read_csv(csv_path, keep_default_na=False, na_values=[""])

    # Cast boolean columns to integers (0/1) for MSSQL BIT columns
    bool_cols = df.select_dtypes(include='bool').columns
    for col in bool_cols:
        df[col] = df[col].astype(int)

    df.to_sql(
        name=table_name,
        con=connection,
        schema='dbo',
        if_exists='append',
        index=False,
        chunksize=1000
    )
    print(f"Loaded {len(df):,} rows into {table_name}.")


def reload_all_tables():
    tables_to_clear = ("events", "sessions", "subscriptions", "features", "users")
    tables_to_load = (
        ("data/raw/users.csv", "users"),
        ("data/raw/features.csv", "features"),
        ("data/raw/sessions.csv", "sessions"),
        ("data/raw/events.csv", "events"),
        ("data/raw/subscriptions.csv", "subscriptions"),
    )

    print("Replacing existing data in dbo.users, dbo.sessions, dbo.events, dbo.features, and dbo.subscriptions...")
    with engine.begin() as connection:
        for table_name in tables_to_clear:
            connection.execute(text(f"DELETE FROM dbo.{table_name}"))

        for csv_path, table_name in tables_to_load:
            load_table(connection, csv_path, table_name)


if __name__ == "__main__":
    reload_all_tables()
    print("All tables successfully reloaded into SQL Server.")