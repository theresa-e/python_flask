from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if len(request.form['name']) < 1:
        flash("Validation error: Enter a valid name.")
    else: 
        flash(f"Thank you, {request.form['name']}.")
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
