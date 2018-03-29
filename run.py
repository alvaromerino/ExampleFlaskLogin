from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# Hardcoded users
USERS = [{'id': 'yoni', 'password': '1234'}]

# We init the login manager
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, id, password):
        self.id = id
        self.password = password

    def __repr__(self):
        return "{}".format(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        idx = 0
        user_found = False
        while user_found is False and idx < len(USERS):
            usr_temp = USERS[idx]
            if usr_temp['id'] == username and usr_temp['password'] == password:
                user_found = True
                user = User(username, password)
                login_user(user)

            idx = idx + 1

        if user_found == True:
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
            return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User(id, None)


if __name__ == '__main__':
    app.run(debug=True)