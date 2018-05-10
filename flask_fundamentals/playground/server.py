from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the index page'

@app.route('/play/<x>')
def more_boxes(x):
    return render_template('index.html', num=int(x))
    
@app.route('/play/<x>/<color>')
def green_boxes(x, color):
    return render_template('index.html', num=int(x), color=str(color))

app.run(debug=True)
