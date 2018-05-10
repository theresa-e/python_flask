from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "HousePinwheel57"
mysql = connectToMySQL('friendsdb')

@app.route('/')
def index():
    all_friends = mysql.query_db("SELECT * FROM friends;")
    print("Got all friends: ", all_friends)
    return render_template('index.html', db=all_friends)

@app.route('/create_friend', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    print(mysql.query_db("SELECT * FROM friends;"))
    mysql.query_db(query, data)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

