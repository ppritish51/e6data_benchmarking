import os
from e6data_python_connector import Connection

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Load environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
PORT = int(os.getenv('PORT', 80))
CATALOG = os.getenv('CATALOG', 'glue')


def test_connection():
    try:
        conn = Connection(
            host=HOST,
            port=PORT,
            username=USERNAME,
            database=DATABASE,
            password=PASSWORD,
            catalog=CATALOG
        )

        # Fetch and print all databases
        databases = conn.get_schema_names(catalog=CATALOG)
        print("Databases available:", databases)

        # Fetch and print tables for each database
        for db in databases:
            print(f"\nTables in database '{db}':")
            tables = conn.get_tables(database=db, catalog=CATALOG)
            for table in tables:
                print(f" - {table}")

        # Close the connection
        conn.close()
        print("\nConnection test successful.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    test_connection()
