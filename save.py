from flask import Flask, render_template, redirect, request, url_for
from flask_login import (LoginManager, UserMixin, login_user, logout_user, login_required, current_user)

app = Flask(__name__)


app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_users():
    return [
        # id пользователя - всегда СТРОКА !!!
            {"id": "0", "username": "user1", "password": "pass1111"},
            {"id": "1", "username": "user2", "password": "pass2"},
            {"id": "2", "username": "KEFedorov", "password": "best_password"}
        ]

class User(UserMixin):
    def __init__(self, user_id):
        # user_id - всегда СТРОКА !!!
        users = get_users()
        for user in users:
            if user["id"] == user_id:
                self.id = user_id
                self.username = user["username"]
                if user["username"] == "KEFedorov":
                    self.is_admin = True
                else:
                    self.is_admin = False

@login_manager.user_loader
def load_user(user_id):
    # user_id - всегда СТРОКА !!!
    users = get_users()
    for user in users:
        if user["id"] == user_id:
            return User(user_id)
    # Если user_id некорректный, то нужно вернуть None
    return None


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/profile')
@login_required
def profile():
    return f'''
    <b>Личный кабинет пользователя (защищенная страница)</b><br>
    Ваш логин: { current_user.username }<br>
    <a href="/logout">Выйти</a>'''


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin_panel():
    if current_user.is_admin:
        return '''
        <b>Панель администратора</b><br>
        Защищенная страница, доступная только администратору
        '''
    else:
        # Ошибка доступа
        abort(403)




@app.route('/register', methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        data = dict(request.form)
        del data['rep_password']
        print(data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        users = get_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                print(user["id"])
                cur_user = User(user["id"])
                print(cur_user)
                login_user(cur_user)
                return redirect(url_for('profile'))

        return 'Неверные данные! <a href="/login">Попробовать снова</a>'

#=================================================================================================

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")