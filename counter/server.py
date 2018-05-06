from flask import Flask, render_template, request, redirect, session,
app = Flask (__name__)
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    if 'count' not in session:
        session['count'] = 0
    session['count'] += 1
    print (session)
    return render_template("index.html")

@app.route('/addtwo')
def add_two():
    session['count'] += 1
    return redirect ("/")

@app.route('/reset')
def reset():
    session['count'] = 0
    return redirect ("/")

if __name__=="__main__":
    app.run(debug=True)