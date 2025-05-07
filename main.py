from flask import Flask, render_template, request,redirect,session
from admin import check_admin,create_admin
from food import get_foods,get_food_by_id,get_orders_for_product

app = Flask(__name__)

app.secret_key='some secret'

@app.route('/')
def index_page():
    foods = get_foods()
    return render_template('index.html',foods=foods)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth_page():
    email = request.form['email']
    password = request.form['password']
    is_admin = check_admin(email, password)
    if is_admin:
        session['user'] = email
        return redirect('/user')
    else:
        return render_template('login.html', message='Invalid email or password')

@app.route('/logout')
def logout_page():
    session.pop('user')
    return redirect('/')

@app.route('/user')
def user_page():
    if 'user' in session:
        return render_template('user.html', user=session['user'])
    else:       
        return redirect('/login')    

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_admin():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return render_template('register.html', message='Please fill in all fields.')

    try:
        create_admin(email, password)
        return redirect('/login')  
    except ValueError as e:
        return render_template('register.html', message=str(e))
    except Exception as e:
        return render_template('register.html', message=f'Registration failed: {e}')

@app.route('/author')
def author_page():
    author_info = {
        'name': 'Mikheil',  
        'surname': 'Ujerashvili', 
        'image': 'https://scontent.ftbs6-2.fna.fbcdn.net/v/t39.30808-1/427990862_3613669265574536_812782898407645130_n.jpg?stp=cp6_dst-jpg_s200x200_tt6&_nc_cat=102&ccb=1-7&_nc_sid=e99d92&_nc_ohc=WGxGjwFacF4Q7kNvwFFld0o&_nc_oc=AdkeX2hxwDhVgKb83G7qWJIVFFMI6vg39tY4RGIrf54JhuADSQ6I3NSOMAHgjogfPWY&_nc_zt=24&_nc_ht=scontent.ftbs6-2.fna&_nc_gid=mzbqNOO691Z22V7FKqqq5Q&oh=00_AfKmWpOyHcO_XGu_ekjbBDoC9z2HqXzOTIurPhgcsY7UpA&oe=682145FC'  #
    }
    return render_template('author.html', author=author_info)

@app.route('/food/<int:id>')
def product_detail(id):
    food = get_food_by_id(id)
    orders = get_orders_for_product(id) 

    if food:
        return render_template('product.html', food=food, orders=orders)
    else:
        return "Product not found."

if __name__ == '__main__':
    app.run()