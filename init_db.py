import sqlite3
import json

# Connect to SQLite database
con = sqlite3.connect('traveL_data.db')
cur = con.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS travel_info (
    duration INTEGER,
    distance REAL,
    origin TEXT,
    destination TEXT,
    time_of_day TEXT,
    mode TEXT,
    directions TEXT
)
''')

# Insert data
cur.execute('''
INSERT INTO travel_info (duration, distance, origin, destination, time_of_day, mode, directions) VALUES (?, ?, ?, ?, ?, ?, ?)
''', (0, 0, "INIT", "INIT", "INIT", "INIT", "INIT"))

# Commit and close
con.commit()
con.close()