import sqlite3

class User:
    def __init__(self,id, email,password,role):
        self.role = 'user'
        self.email = email
        self.id = id
        self.password = password  

    def __str__(self):
        return f" {self.id} - {self.email} -{self.password} "
    
def get_password_hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()
    
def create_user(email, password):
    connection=sqlite3.connect('food.db')
    password_hash = get_password_hash(password)
    cursor=connection.cursor()
    try:
        cursor.execute("SELECT email FROM user WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            raise ValueError(f"User with email '{email}' already exists.")
        else:
            cursor.execute("INSERT INTO user   (email, password) VALUES (?, ?)", (email, password_hash))
            connection.commit()
            print(f"user   '{email}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: use with email '{email}' already exists.")
        raise Exception(f"user with email '{email}' already exists.")
    finally:
        connection.close()

def check_user(email, password):
    connection = sqlite3.connect('food.db')
    password_hash = get_password_hash(password)
    sql = "SELECT * FROM user  WHERE email = ? AND password = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (email, password_hash))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def get_user_by_email(email):
    conn = sqlite3.connect('food.db')
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def update_user_password(user_id, new_password):
    connection = sqlite3.connect('food.db')
    cursor = connection.cursor()
    sql = "UPDATE user SET password = ? WHERE id = ?"
    cursor.execute(sql, (new_password, user_id))
    connection.commit()
    connection.close()



