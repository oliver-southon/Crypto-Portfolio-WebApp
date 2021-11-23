import sqlite3 as sql 

conn = sql.connect('trades.db')
c= conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS trades (
        holding_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        entry_price REAL NOT NULL,
        entry_amt REAL NOT NULL,
        date TEXT,
        PRIMARY KEY (holding_id)
    )
    """
)

conn.close()