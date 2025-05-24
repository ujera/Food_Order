import sqlite3

class Food:
    def __init__(self, id, name, image, description, price):
        self.name = name
        self.id = id
        self.price = price
        self.image = image
        self.description = description

    def __str__(self):
        return f" {self.id} - {self.name} -{self.price} - {self.image} - {self.description} "
    
def get_foods():
    connection = sqlite3.connect('Food.db')
    sql = "SELECT * FROM Food"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    foods = []
    for row in result:
        food = Food(row[0], row[1], row[2], row[3], row[4])
        foods.append(food)
    return foods

def create_food(name, image, description, price):
    connection = sqlite3.connect('Food.db')
    sql = f"INSERT INTO Food (name, image, description, price) VALUES ('{name}', '{image}', '{description}', {price})"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

def get_food_by_id(food_id):
    connection = sqlite3.connect('Food.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Food WHERE id = ?", (food_id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return Food(row[0], row[1], row[2], row[3], row[4])
    return None


def get_orders_for_product(product_id):
    connection = sqlite3.connect('Food.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, name, surname, email, address, paymentmethod
        FROM `Order`
        WHERE foodid = ?
    """, (product_id,))
    orders_data = cursor.fetchall()
    connection.close()
    return orders_data

def delete_food(food_id):
    connection = sqlite3.connect('Food.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Food WHERE id = ?", (food_id,))
    connection.commit()
    connection.close()

def update_food(food_id, name, description, price):
    connection = sqlite3.connect('Food.db')
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Food
        SET name = ?, price = ?, description = ?
        WHERE id = ?
    """, (name, price, description, food_id))
    connection.commit()
    connection.close()
def get_all_foods():
    connection = sqlite3.connect('Food.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Food")
    rows = cursor.fetchall()
    connection.close()
    return rows
