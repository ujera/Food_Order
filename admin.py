import sqlite3
class Admin:
    def __init__(self,id, email,password):
        self.email = email
        self.id = id
        self.password = password  

    def __str__(self):
        return f" {self.id} - {self.email} -{self.password} "
    
def get_password_hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()
    
def create_admin(email, password):
    connection=sqlite3.connect('food.db')
    password_hash = get_password_hash(password)
    cursor=connection.cursor()
    try:
        cursor.execute("SELECT email FROM admin WHERE email = ?", (email,))
        existing_admin = cursor.fetchone()

        if existing_admin:
            raise ValueError(f"Admin with email '{email}' already exists.")
        else:
            cursor.execute("INSERT INTO admin (email, password) VALUES (?, ?)", (email, password_hash))
            connection.commit()
            print(f"Admin '{email}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Admin with email '{email}' already exists.")
        raise Exception(f"Admin with email '{email}' already exists.")
    finally:
        connection.close()

def check_admin(email, password):
    connection = sqlite3.connect('food.db')
    password_hash = get_password_hash(password)
    sql = "SELECT * FROM admin WHERE email = ? AND password = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (email, password_hash))
    result = cursor.fetchone()
    connection.close()
    return result is not None

