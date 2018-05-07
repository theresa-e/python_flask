from flask import Flask, render_template, request, redirect, flash, session
app = Flask(__name__)
app.secret_key = "HousePinwheel57"

@app.route('/')
def index():
    print(session)
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def survey_results():
    if len(request.form['name']) < 1:
        flash("Enter a valid name.")
    if len(request.form['location']) < 1:
        flash("Enter a valid location.")
    if len(request.form['comments']) > 120:
        flash("Comments must be 120 characters or less. Please adjust and resubmit.")
        session['comments'] = request.form['comments']
        print(session)
    else:
        print(session)
        return render_template('result.html')
    return redirect('/')

@app.route('/danger')
def danger():
    print('\n\n\nA user tried to visit /danger. They are being redirected back to /.')
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)