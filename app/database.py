import sqlite3

conn = sqlite3.connect("data/security_lab.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID TEXT PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        department TEXT NOT NULL,
        jobTitle TEXT NOT NULL
    )
""")

cursor.execute("""
    INSERT OR IGNORE INTO users
    (userID, firstName, lastName, department, jobTitle)
    VALUES (?, ?, ?, ?, ?)
""", ("1001", "Isaac", "Cardoso", "Security", "IAM Engineer"))

conn.commit()
conn.close()

def get_all_users():
    conn = sqlite3.connect("data/security_lab.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    
    users = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return users


