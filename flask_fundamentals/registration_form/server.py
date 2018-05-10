from flask import Flask, render_template, request, redirect, flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NUMBER_REGEX = re.compile(r'[a-zA-Z]')
app = Flask(__name__)
app.secret_key = "HousePinwheel57"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitform', methods=['POST'])
def submit():
    # check to see that all fields are filled with proper length
    if len(request.form['email']) < 1:
        flash("Please provide an email.")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Enter a valid email address.")
    if len(request.form['f_name']) < 1:
        flash("Please provide your first name.")
    elif not NUMBER_REGEX.match(request.form['f_name']):
        flash("Enter a valid first name.")
    if len(request.form['l_name']) < 1:
        flash("Please provide your last name.")
    elif not NUMBER_REGEX.match(request.form['l_name']):
        flash("Enter a valid last name.")
    if len(request.form['password']) < 8 or len(request.form['confirm-password']) < 8 :
        flash("Password must be at least 8 characters long.")
    elif request.form['password'] != request.form['confirm-password']:
        flash("Passwords do not match.")
    else:
        flash("Thanks for submitting your information!")
        return redirect ('/')

    return redirect('/')
if __name__=="__main__":
    app.run(debug=True)