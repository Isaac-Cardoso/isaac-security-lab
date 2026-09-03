import sqlite3


def get_all_users():
    conn = sqlite3.connect("data/security_lab.db")
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        
        users = [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
    return users

def create_user(userID, firstName, lastName, department, jobTitle):
    conn = sqlite3.connect("data/security_lab.db")
    
    try:
        cursor = conn.cursor()
    
        cursor.execute("""
            INSERT INTO users
            (userID, firstName, lastName, department, jobTitle)
            values (?, ?, ?, ?, ?)
        """, (userID, firstName, lastName, department, jobTitle))
    
        conn.commit()
        conn.close()
    
        return {
            "userID": userID,
            "firstName": firstName,
            "lastName": lastName,
            "department": department,
            "jobTitle": jobTitle
        }
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect("data/security_lab.db")
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE userID = ?", (user_id,))
        
        user = cursor.fetchone()
    finally:
        conn.close()
    
    if user:
        return dict(user)
    
    return None

def update_user_by_id(user_id, updates):
    conn = sqlite3.connect("data/security_lab.db")
    
    try:
        cursor = conn.cursor()
        
        set_clauses = []
        values = []
        for field, value in updates.items():
            set_clauses.append(f"{field} = ?")
            values.append(value)
        
        set_clause = ", ".join(set_clauses)
        values.append(user_id)
        
        cursor.execute(f"UPDATE users SET {set_clause} WHERE userID = ?", values)
        
        conn.commit()
    finally:
        conn.close()

