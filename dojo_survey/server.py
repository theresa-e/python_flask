from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def survey_results():
    name = request.form['name']
    return render_template('result.html')

if __name__=="__main__":
    app.run(debug=True)