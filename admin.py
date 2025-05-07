import sqlite3
class Admin:

    def __init__(self,id, email,password):
        self.role = 'admin'
        self.email = email
        self.id = id
        self.password = password  

    def __str__(self):
        return f" {self.id} - {self.email} -{self.password} "
    
def get_admin_by_email(email):
    conn = sqlite3.connect('food.db')
    conn.row_factory = sqlite3.Row
    admin = conn.execute("SELECT * FROM admin WHERE email = ?", (email,)).fetchone()
    conn.close()
    return admin