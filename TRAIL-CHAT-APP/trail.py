from flask import Flask, render_template, request, redirect, g, session, url_for
import os
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == '12345':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))

    
    return render_template('index.html')

@app.route('/register')
def about():
    return render_template('register.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')


@app.route('/protected')
def protected():
    if g.user:
        return render_template('session.html', user=session['user'])
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']
    # return render_template('session.html')

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return render_template('index.html')



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)






if __name__ == '__main__':
    socketio.run(app, debug=True)
