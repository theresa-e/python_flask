from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt    
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]')
app = Flask(__name__)
app.secret_key = "HousePinwheel57"
bcrypt = Bcrypt(app)
mysql = connectToMySQL('login_reg_db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def validate():
    # Save entered user info in session:
    if 'first_name' not in session:
        session['first_name'] = request.form['first_name']
    if 'last_name' not in session:
        session['last_name'] = request.form['last_name']
    if 'email' not in session:
        session['email'] = request.form['email']
    # Validate the user input. 
    if len(request.form['first_name']) < 1:
        flash('Please enter a first name.', 'first_name')
    elif len(request.form['first_name']) <= 2:
        flash('First name must be at least two characters.', 'first_name')
    elif not NAME_REGEX.match(request.form['first_name']):
        flash('Please enter a valid first name. No numbers allowed. ', 'first_name')
    if len(request.form['last_name']) < 1:
        flash('Please enter a last name.', 'last_name')
    elif len(request.form['last_name']) <= 2:
        flash('Last name must be at least two characters.', 'last_name')
    elif not NAME_REGEX.match(request.form['last_name']):
        flash('Please enter a valid last name.', 'last_name')
    if len(request.form['email']) < 1:
        flash('Email cannot be blank.', 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address.', 'email')
    if len(request.form['password']) < 1:
        flash('Password cannot be blank.', 'password')
    elif len(request.form['password']) < 8:
        flash('Password must be at least 8 characters.', 'password')
    if len(request.form['password_confirm']) < 1:
        flash('Password cannot be blank.', 'password_confirm')
    elif len(request.form['password_confirm']) < 8:
        flash('Password must be at least 8 characters.', 'password_confirm')
    elif request.form['password'] != request.form['password_confirm']:
        flash('Passwords do not match. Please resubmit.', 'password_confirm')
    # Run query to check if the user's email is in our db.
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { 
        "email" : request.form['email']
        }
    results = mysql.query_db(query, data)
    # If the user exists in our db, we'll ask them to login using their email. 
    if results:
        flash('The email ' + request.form['email'] + ' belongs to a registered account. Please login using ' + request.form['email'], 'notice')
    # If the query returns no results, we'll add them as a new account. This is a new user!
    else:
        if 'email' not in session:
            session['email'] = request.form['email']
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
        }
        mysql.query_db(query, data)
        return redirect ('/new_user')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # Add input to session so user will not have to input again. 
    if 'login_email' not in session:
        session['login_email'] = request.form['login_email']
    if len(request.form['login_email']) < 1:
        flash('Email cannot be blank.', 'login_email')
    elif not EMAIL_REGEX.match(request.form['login_email']):
        flash('Invalid email address.', 'login_email')
    if len(request.form['login_password']) < 1:
        flash('Password cannot be blank.', 'login_password')
    elif len(request.form['login_password']) < 8:
        flash('Password must be at least 8 characters.', 'login_password')

    # After validating user input, we check that the email belongs to an account.
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
        'email' : request.form['login_email']
        }
    result = mysql.query_db(query, data)

    # After validating that the account exists, hash the given password and check if it matches our db hash. 
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['login_password']):
            return redirect('/success')
        else:
            flash('You could not be logged in.', 'login')
            return redirect('/')
    else:
        flash('Email does not belong to an account. Please register before logging in.', 'login')
        return redirect ('/')


@app.route('/success')
def returning_user():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
        'email' : session['login_email']
        }
    result = mysql.query_db(query, data)
    return render_template('/success.html', results=result)

@app.route('/new_user')
def welcome_new_user():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
        'email' : session['email']
        }
    result = mysql.query_db(query, data)
    return render_template('/success.html', results=result)

def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

