from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, UserMixin


app = Flask(__name__)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']

        if user_id == 'admin' and password == 'admin':
            user = User(user_id)
            login_user(user)
            return render_template('dashboard.html',username=user_id)
        else:
            error = 'Invalid username or password'
            return render_template('home.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
