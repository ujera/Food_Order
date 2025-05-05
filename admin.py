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
    sql=f"INSERT INTO admin (email, password) VALUES ('{email}', '{password_hash}')"
    cursor=connection.cursor()
    cursor.execute(sql)
    connection.commit()
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

