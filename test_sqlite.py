import sqlite3

print("Testing SQLite connection...")
try:
    conn = sqlite3.connect('test.db')
    print("SQLite connection successful!")
    conn.close()
    print("Connection closed.")
except Exception as e:
    print(f"Error: {e}")

print("Script completed.")