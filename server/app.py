import os
from flask import Flask, request, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
app.config['dev_mode'] = True
app.config['sqlite_path'] = 'app.db'
import model
from model import User
db = model.db_factory(app.config)

auth = Auth(app, login_url_name='index')

#@login_required()
def admin():
    return 'Admin! Excellent!'

def index():
    if request.method == 'POST':
        username = request.form['username']

        try:
            user = db.query(User).filter(User.username==username).one()
        except NoResultFound:
			user = None 
        if user is not None:
            # Authenticate and log in!
            if user.authenticate(request.form['password']):
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
        if db.query(User).filter(User.username==username).first():
            return 'User already exists.'
        password = request.form['password']
        user = User(username=username, password=password)
        db.add(user)
        return redirect(url_for('index'))
    return '''
            <form method="POST">
                Username: <input type="text" name="username"/><br/>
                Password: <input type="password" name="password"/><br/>
                <input type="submit" value="Create"/>
            </form>
        '''

def logout_view():
    user_data = logout()
    if user_data is None:
        return 'No user to log out.'
    return 'Logged out user {0}.'.format(user_data['username'])

# URLs
app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/admin/', 'admin', admin)
app.add_url_rule('/users/create/', 'user_create', user_create, methods=['GET', 'POST'])
app.add_url_rule('/logout/', 'logout', logout_view)

# Secret key needed to use sessions.
app.secret_key = 'N4BUdSXUzHxNoO8g'

if __name__ == '__main__':
    try:
        open('app.db')
    except IOError:
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
