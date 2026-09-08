import sqlite3

def get_db_connection():
    conn = sqlite3.connect("data/security_lab.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_all_users():
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        
        users = [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
    return users

def create_user(userID, firstName, lastName, department, jobTitle):
    conn = get_db_connection()
    
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
    conn = get_db_connection()

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
    conn = get_db_connection()
    
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

def set_lifecycle_state(user_id, lifecycle_state):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET lifecycleState = ? WHERE userID = ?", (lifecycle_state, user_id))

        conn.commit()
    finally:
        conn.close()

def assign_role_to_user(user_id, role_id):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_roles (userID, roleID) VALUES (?, ?)", 
            (user_id, role_id))

        conn.commit()
    finally:
        conn.close()

def get_role_by_id(role_id):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM roles WHERE roleID = ?",
            (role_id,)
        )

        role = cursor.fetchone()
    finally:
        conn.close()

    if role:
        return dict(role)

    return None

def get_roles_for_user(user_id):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT r.* FROM roles r
            JOIN user_roles ur ON r.roleID = ur.roleID
            WHERE ur.userID = ?
            """,
            (user_id,)
        )

        roles = [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

    return roles

def remove_role_from_user(user_id, role_id):
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_roles WHERE userID = ? AND roleID = ?",
            (user_id, role_id)
        )
        deleted = cursor.rowcount
        conn.commit()
    finally:
        conn.close()

    return deleted > 0