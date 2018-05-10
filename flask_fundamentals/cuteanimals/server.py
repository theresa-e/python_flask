from flask import Flask, render_template, redirect
from random import shuffle 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/danger')
def danger():
    print('\n\nThis is a danger page. Redirecting you back to safety!\n\n')
    return redirect ('/')
@app.route('/random/<num>')
def random_imgs(num):
    shuffled_images = shuffle_list(int(num))
    return render_template('random.html', images=shuffled_images)
def shuffle_list(max):
    list = []
    for i in range(max):
        list.append(i+1)
    shuffle(list)
    return list

if __name__=="__main__":
    app.run(debug=True)