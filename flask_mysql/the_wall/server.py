from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt    
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z0-9_-]*$')
app = Flask(__name__)
app.secret_key = "HousePinwheel57"
bcrypt = Bcrypt(app)
mysql = connectToMySQL('thewall')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # Validate user input
    if len(request.form['first_name']) < 1:
        flash('First name cannot be blank', 'first_name')
    elif len(request.form['first_name']) <=2 :
        flash('Please enter a valid first name of at least 2 characters.', 'first_name')
    if len(request.form['last_name']) < 1:
        flash('Last name cannot be blank', 'last_name')
    elif len(request.form['last_name']) <=2 :
        flash('Please enter a valid last name of at least 2 characters.', 'last_name')
    if len(request.form['reg_email']) < 1:
        flash('Please enter an email address', 'email')
    elif not EMAIL_REGEX.match(request.form['reg_email']):
        flash('Invalid email address, please resubmit.', 'email') 
    if len(request.form['password']) < 1:
        flash('Password enter a password.', 'password')
    elif len(request.form['password']) < 8:
        flash ('Password should be at least 8 characters.', 'password')
    if request.form['password'] != request.form['password_confirm']:
        flash ('Passwords do not match. Please resubmit.', 'password_confirm')

    # Save user input in session
    if 'first_name' not in session:
        session['first_name'] = request.form['first_name']
    session['first_name'] = request.form['first_name']
    if 'last_name' not in session:
        session['last_name'] = request.form['last_name']
    session['last_name'] = request.form['last_name']
    if 'reg_email' not in session:
        session['reg_email'] = request.form['reg_email']
    session['reg_email'] = request.form['reg_email']

    # Run a query to see if the email is already associated with an account. 
    query = "SELECT * FROM users WHERE email =%(email)s;"
    data = {
        "email" : request.form['reg_email']
    }
    results= mysql.query_db(query, data)
    print(len(results))

    # If it is not, add user to our database. 
    if len(results) == 0:
        if len(request.form['password']) > 0:
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            query = "INSERT INTO users (first_name, last_name, email, password, create_at, update_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
            data = {
                    'first_name': request.form['first_name'],
                    'last_name': request.form['last_name'],
                    'email': request.form['reg_email'],
                    'password': pw_hash,
                    }
            mysql.query_db(query, data)
        else:
            return redirect('/')
        return redirect('/success')

    # If it is, clear session and ask them to login instead of registering. 
    else:
        session.clear()
        flash('The email address ' + request.form['reg_email'] + ' is already associated with an account. Please login or use a different email address. ', 'notice')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # Save user input in session
    if 'login_email' not in session:
        session['login_email'] = request.form['login_email']
    session['login_email'] = request.form['login_email']

    # Validate user input
    if len(request.form['login_email']) < 1:
        flash('Please enter an email.', 'login_email')
    elif not EMAIL_REGEX.match(request.form['login_email']):
        flash('Invalid email address, please resubmit.', 'login_email') 
    print('TEST THIS FUNCTION')
    # return redirect ('/')
    # Run a query to see if the email is in our database. 
    query = "SELECT * FROM users WHERE email =%(email)s;"
    data = {
        "email" : request.form['login_email']
    }
    results= mysql.query_db(query, data)
    if 'userid' not in session:
        session['userid'] = results[0]['id']
    session['userid'] = results[0]['id']

    # If our query returns 0 results, the user does not exist in our database. Allow them to register.
    if len(results) == 0:
        flash('You could not be logged in.', 'login')
        return redirect('/')
    else:
        if bcrypt.check_password_hash(results[0]['password'], request.form['login_password']):
            return redirect('/success')
        else:
            flash('You could not be logged in.', 'login')
    return redirect ('/')

@app.route('/success')
def user():
    if 'reg_email' not in session:
            session['reg_email'] = session['login_email']
    else:
        session['reg_email'] = session['login_email']
    query = "SELECT * FROM users WHERE email =%(email)s;"
    data = {
        "email" : session['reg_email']
    }
    results= mysql.query_db(query, data)
    if 'userid' not in session:
        session['userid'] = results[0]['id']
    session['userid'] = results[0]['id']
    message_query = "SELECT u.id as 'user_id', u.first_name, u.last_name, m.message, m.id as 'message_id', m.create_at FROM users u LEFT JOIN messages m ON u.id = m.users_id ORDER BY m.create_at DESC;"
    message_results = mysql.query_db(message_query)
    user_query = "SELECT first_name, last_name, id FROM users WHERE id = %(userid)s;"
    userdata = {
        'userid' : session['userid']
    }
    user_data = mysql.query_db(user_query, userdata)
    post_comment_query = "SELECT * FROM comments"
    post_comment_results = mysql.query_db(post_comment_query)
    return render_template('wall.html', message_results=message_results, user_data=user_data, post_comment_results=post_comment_results)

@app.route('/post', methods=['POST'])
def post():
    return redirect ('/success')

@app.route('/post_message', methods=['POST'])
def post_message():
    debugHelp('LOOK AT SESSION')
    print('------------.', request.form['message'])
    if 'message' not in session:
        session['message'] = request.form['message']
    else:
        session['message'] = request.form['message']
    debugHelp('LOOK AT SESSION')
    query = "INSERT INTO messages (message, create_at, updated_at, users_id) VALUES (%(message)s, NOW(), NOW(), %(users_id)s);"
    data = {
            "message" : session['message'],
            "users_id" : session['userid']
            }
    mysql.query_db(query, data)
    return redirect ('/success')

@app.route('/post_comment', methods=['POST'])
def post_comment():
    post_comment_query = "INSERT INTO comments (comment, create_at, updated_at, messages_id, users_id) VALUES (%(user_comment)s, NOW(), NOW(), %(message_id)s, %(users_id)s);"
    post_comment_data = {
        "user_comment" : request.form['comment'],
        "message_id" : int(request.form['message_id']),
        "users_id" : session['userid']
    }
    mysql.query_db(post_comment_query, post_comment_data)
    return redirect ('/success')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect ('/')

@app.route('/test')
def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)

if __name__=="__main__":
    app.run(debug=True)