import sqlite3
class Order:
    def __init__(self, id,foodid, name, surname, email, address, paymentmethod):   
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.address = address
        self.paymentmethod = paymentmethod
        self.foodid = foodid
    def __str__(self):
        return f" {self.id} - {self.name} -{self.surname} - {self.email} - {self.address} - {self.paymentmethod} "
def get_db_connection():
    conn = sqlite3.connect('Food.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def create_order(user_id, food_id, name, surname, email, address, payment_method):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            INSERT INTO `Order` (userid, foodid, name, surname, email, address, paymentmethod)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, food_id, name, surname, email, address, payment_method),
        )
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise ValueError(f"Failed to create order: {e}")
    finally:
        conn.close()



def get_orders():
    conn = get_db_connection()
    try:
        orders = conn.execute("SELECT * FROM `Order`").fetchall()
        return orders
    except sqlite3.Error as e:
        raise ValueError(f"Failed to retrieve orders: {e}")
    finally:
        conn.close()



def get_order_by_id(order_id):
    conn = get_db_connection()
    try:
        order = conn.execute("SELECT * FROM `Order` WHERE id = ?", (order_id,)).fetchone()
        return order
    except sqlite3.Error as e:
        raise ValueError(f"Failed to retrieve order: {e}")
    finally:
        conn.close()



def delete_order(order_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM `Order` WHERE id = ?", (order_id,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise ValueError(f"Failed to delete order: {e}")
    finally:
        conn.close()

