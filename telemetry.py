import sqlite3
import os

def log_scan_metadata(vulnerability_type, language, timestamp):
    db_path = 'telemetry.sqlite'
    
    # Connect and automatically create the file if missing
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vulnerability_type TEXT NOT NULL,
                language TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        # Insert the silent telemetry data
        cursor.execute('''
            INSERT INTO scan_log (vulnerability_type, language, timestamp)
            VALUES (?, ?, ?)
        ''', (vulnerability_type, language, timestamp))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database execution error: {e}")
    finally:
        conn.close()