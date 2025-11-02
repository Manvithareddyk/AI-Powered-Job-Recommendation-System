import sqlite3

# Connect to the database and add error handling
conn = None
try:
    conn = sqlite3.connect('job_recommender.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create resumes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        skills TEXT NOT NULL,
        education TEXT,
        work_experience TEXT,
        preferred_location TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # Commit changes
    conn.commit()
    print("Database tables created successfully!")
except sqlite3.Error as e:
    print(f"Error creating database: {e}")
finally:
    # Ensure connection is closed even if an error occurs
    if conn:
        conn.close()

print("Script execution completed!")