from flask import Flask, render_template, request, redirect, session
import random, time
app = Flask (__name__)
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    # player current score
    if 'total_gold' not in session:
        session['total_gold'] = 0
    if 'status' not in session:
        session['status'] = []
    return render_template('index.html', total_gold=session['total_gold'], status=session['status'])

@app.route('/process_money', methods=['POST'])
def process_money():
    # if player goes to farm
    if request.form['building'] == 'farm':
        total_won = random.randrange(5,10)
        session['total_gold'] += total_won
        session['status'].append('You earned +' + str(total_won) + ' gold on ' + str(time.strftime('%b %d, %Y, %H:%M%p ')))
        return redirect ('/')
    # if player goes to cave 
    if request.form['building'] == 'cave':
        total_won = random.randrange(5,10)
        session['total_gold'] += total_won
        session['status'].append('You earned +' + str(total_won) + ' gold on ' + str(time.strftime('%b %d, %Y, %H:%M%p ')))
        return redirect ('/')
    # if player goes to house
    if request.form['building'] == 'house':
        total_won = random.randrange(2, 5)
        session['total_gold'] += total_won
        session['status'].append('You earned +' + str(total_won) + ' gold on ' + str(time.strftime('%b %d, %Y, %H:%M%p ')))
        return redirect ('/')
    # if player goes to casino
    if request.form['building'] == 'casino':
        total_won = random.randrange(0, 20) - 10
        session['total_gold'] += total_won
        if total_won >= 0:
            session['status'].append('You earned +' + str(total_won) + ' gold on ' + str(time.strftime('%b %d, %Y, %H:%M%p ')))
        else:
            session['status'].append('You lost ' + str(total_won) + ' gold on ' + str(time.strftime('%b %d, %Y, %H:%M%p ')))
        return redirect ('/')

if __name__=='__main__':
    app.run(debug=True)