from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def survey_results():
    name = request.form['name']
    return render_template('result.html')

@app.route('/danger')
def danger():
    print('\n\n\nA user tried to visit /danger. They are being redirected back to /.')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)