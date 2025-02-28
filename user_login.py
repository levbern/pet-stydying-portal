from flask import Flask, render_template, redirect, url_for, request, abort
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
def home():
    return '''
    Главная страница<br>
    <a href="/login">Войти</a><br>
    <a href="/profile">Профиль</a><br>
    <a href="/admin">Панель администратора</a>
    '''




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


if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1", debug=True)