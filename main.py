from flask import Flask, render_template, request,redirect,session
from admin import check_admin

app = Flask(__name__)

app.secret_key='some secret'

@app.route('/')
def index_page():
    return render_template('index.html')

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

        


if __name__ == '__main__':
    app.run()