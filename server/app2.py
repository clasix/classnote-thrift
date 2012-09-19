import os
from flask import Flask, request, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
from ctrl import Ctrl

app = Flask(__name__)
app.config['dev_mode'] = True
app.config['sqlite_path'] = 'app2.db'
import model
from model import User, AuthToken
db = model.db_factory(app.config)

ctrl = Ctrl(db)

#@login_required()
def admin():
    return 'Admin! Excellent!'

def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        auth_token = ctrl.login_by_username(username, password)

        if auth_token is not None:
            print 'auth_token is %s.' % auth_token
            return redirect(url_for('admin'))
        return 'Failure :('
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Log in"/>
            </form>
        '''

def user_create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        res = ctrl.sign_up_username(username, password)
        if res:
            return redirect(url_for('index'))
        return redirect(url_for('user_create'))
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Create"/>
            </form>
        '''

def logout_view():
    auth_token = request.args.get('auth_token', None)

    res = ctrl.sign_out(auth_token)
    if res:
        return 'Logged out auth_token %s.' % auth_token
    return 'No user to log out.'

# URLs
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/admin/', 'admin', admin)
app.add_url_rule('/users/create/', 'user_create', user_create, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout_view)

# Secret key needed to use sessions.
app.secret_key = 'N4BUdSXUzHxNoO8g'

if __name__ == '__main__':
    try:
        open('app2.db')
    except IOError:
        pass #db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
