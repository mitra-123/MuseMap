import sqlite3
import os

DB_PATH = "database/graph.db"
SCHEMA_PATH = "database/schema.sql"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    
    conn = get_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized succesfully")

if __name__ == "__main__":
    init_db()

