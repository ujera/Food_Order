from flask import Flask, render_template, request,redirect,session,url_for, abort
from user import create_user,get_user_by_email
from food import get_foods,get_food_by_id,get_orders_for_product,create_food,delete_food,update_food
from admin import get_admin_by_email
import hashlib
from order import create_order,get_orders,get_order_by_id,delete_order

app = Flask(__name__)

app.secret_key='some secret'

def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()
def check_password(stored_password, provided_password):
    """Verifies a provided password against a stored SHA256 hash."""
    hashed_provided_password = hash_password(provided_password)
    return hashed_provided_password == stored_password

@app.route('/')
def index_page():
    foods = get_foods()
    return render_template('index.html', foods=foods)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth_page():
    email = request.form['email']
    password = request.form['password']

    admin = get_admin_by_email(email)
    if admin and check_password(admin['password'], password):
        session['user_id'] = admin['id']
        session['user_email'] = admin['email']
        session['user_role'] = 'admin'
        return redirect('/user')

    user = get_user_by_email(email)
    if user and check_password(user['password'], password):
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_role'] = 'user'
        return redirect('/user')

    return render_template('login.html', message='Invalid email or password')


@app.route('/logout')
def logout_page():
    session.clear()
    return redirect('/')

@app.route('/user')
def user_page():
    if 'user_role' in session:
        return render_template('user.html',
                               user_email=session['user_email'],
                               user_role=session['user_role']) 
    return redirect('/login')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return render_template('register.html', message='Please fill in all fields.')
    try:
        create_user(email, password,'user')
        return redirect('/login')
    except ValueError as e:
        return render_template('register.html', message=str(e))
    except Exception as e:
        return render_template('register.html', message=f'User registration failed: {e}')

@app.route('/author')
def author_page():
    author_info = {
        'name': 'Mikheil',
        'surname': 'Ujerashvili',
        'image': 'https://scontent.ftbs6-2.fna.fbcdn.net/v/t39.30808-1/427990862_3613669265574536_812782898407645130_n.jpg?stp=cp6_dst-jpg_s200x200_tt6&_nc_cat=102&ccb=1-7&_nc_sid=e99d92&_nc_ohc=WGxGjwFacF4Q7kNvwFFld0o&_nc_oc=AdkeX2hxwDhVgKb83G7qWJIVFFMI6vg39tY4RGIrf54JhuADSQ6I3NSOMAHgjogfPWY&_nc_zt=24&_nc_ht=scontent.ftbs6-2.fna&_nc_gid=mzbqNOO691Z22V7FKqqq5Q&oh=00_AfKmWpOyHcO_XGu_ekjbBDoC9z2HqXzOTIurPhgcsY7UpA&oe=682145FC'
    }
    return render_template('author.html', author=author_info)

@app.route('/food/<int:id>')
def product_detail(id):
    food = get_food_by_id(id)
    orders = get_orders_for_product(id)
    if food:
        return render_template('product.html', food=food, orders=orders)
    return "Product not found."

@app.route('/product/create', methods=['GET', 'POST'])
def product_create():
    if 'user_role' not in session or session['user_role'] != 'admin':
        abort(403)  # Access denied for non-admins
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']
        try:
            create_food(name, image, description, price)
            return redirect(url_for('index_page'))  # Redirect to product list
        except ValueError as e:
            return render_template('product_create.html', error=str(e))
    return render_template('product_create.html')


@app.route('/product/delete/<int:id>')
def product_delete(id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        abort(403)  # Access denied for non-admins
    try:
        delete_food(id)
        return redirect(url_for('index_page'))  # Redirect to product list
    except ValueError as e:
        return render_template('index.html', error=str(e))  # Or handle as appropriate


@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def product_edit(id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        abort(403)  # Access denied for non-admins

    food = get_food_by_id(id)
    if not food:
        return "Product not found."  # Or handle 404

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        try:
            update_food(id, name, description, price)  # Assuming image is not being updated
            return redirect(url_for('index_page'))  # Redirect
        except ValueError as e:
            return render_template('product_edit.html', food=food, error=str(e))
    return render_template('product_edit.html', food=food)

#orders------------------------------------

@app.route('/order/<int:food_id>', methods=['GET', 'POST'])
def create_order_page(food_id):
    food = get_food_by_id(food_id)
    if not food:
        return "Food not found"

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        address = request.form['address']
        payment_method = request.form['payment_method']

        try:
            create_order(session['user_id'], food_id, name, surname, email, address, payment_method)
            return redirect(url_for('orders_page'))  # Redirect to orders list
        except ValueError as e:
            return render_template('order.html', food=food, error=str(e))

    return render_template('order.html', food=food)  # Show order form



@app.route('/orders')
def orders_page():
    if 'user_role' not in session:
        return redirect(url_for('login_page'))

    orders = get_orders()
    return render_template('orders.html', orders=orders)



@app.route('/orders/<int:order_id>')
def order_detail_page(order_id):
    if 'user_role' not in session:
        return redirect(url_for('login_page'))

    order = get_order_by_id(order_id)
    if not order:
        return "Order not found"
    return render_template('order_detail.html', order=order)



@app.route('/orders/remove/<int:order_id>')
def order_remove(order_id):
    try:
        delete_order(order_id)
        return redirect(url_for('orders_page'))
    except ValueError as e:
        return render_template('orders.html', error=str(e))

if __name__ == '__main__':
    app.run()