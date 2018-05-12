from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "HousePinwheel57"
mysql = connectToMySQL('emaildb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Validates that user has completed field and if input is in emaiil format. 
    if len(request.form['email']) < 1:
        flash('Email cannot be blank.')
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address.')
    # After both conditions are met, we will check if the email entered exists in our database.
    else:
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        data = {
            'email': request.form['email']
            }
        mysql.query_db(query, data)
        print('Length of query is: ', len(mysql.query_db(query, data)))
        # If the email exists in our database, we ask user to enter a new email. 
        if len(mysql.query_db(query, data)) > 0:
            flash('The email ' + request.form['email'] + ' is already in use.')
            return redirect('/')
        # If the email is not in our database, user is allowed to register. 
        # Add email to database and redirect to "member page."
        else:
            query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
            data = {
                    'email': request.form['email']
                    }
            mysql.query_db(query, data)
            return redirect ('/success')
    return redirect('/')

@app.route('/success')
def success():
    all_emails = mysql.query_db("SELECT * FROM emails;")
    return render_template('success.html', emaildb = all_emails)



if __name__=="__main__":
    app.run(debug=True)