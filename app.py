import random
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_login import (LoginManager, UserMixin, login_user, logout_user, login_required, current_user)
import json, os, database
import sqlite3

from uuid import uuid4
app = Flask(__name__)

app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#----------------------------MARKDOWN------------------------------#

@app.route('/markdown', methods=['GET', 'POST'])
def markdown():
    logged_in = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('markdown.html', loggedIn=logged_in)
    else:
        return 0
#-------------------------------------------------------------------#
MESSAGES_FILE = 'messages.json'

#----------------------------------для таблицы github--------------------------------#
@app.route('/github')
def contributions():
    # Пример данных (замените своими)
    data = {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Dec'],
        'contributions': generate_contributions_data(),
        'get_color': lambda value: (
            'var(--purple-20)' if value > 10 else
            'var(--purple-10)' if value > 5 else
            'var(--purple-5)' if value > 0 else
            'var(--purple-0)'
        )
    }
    return render_template('github-activity.html', **data)

def generate_contributions_data():
    # Генерация данных для 53 недель
    return [[{'value': random.randint(0, 15), 'date': '2023-01-05'} 
           for _ in range(7)] for _ in range(53)]

#----------------------------для чата-------------------------------#


@app.route('/get_messages')
def get_messages():
    return jsonify(load_messages())

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    messages = load_messages()
    
    new_message = {
        'id': str(uuid4()),
        'class': 'own' if data['username'] == 'current_user' else 'alien',
        'text': data['text'],
        'username': data['username']
    }
    
    messages.append(new_message)
    save_messages(messages)
    return jsonify({'status': 'success'})

@app.route('/delete_message/<msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    messages = load_messages()
    filtered = [m for m in messages if m['id'] != msg_id]
    
    if len(filtered) == len(messages):
        return jsonify({'status': 'not found'}), 404
    
    save_messages(filtered)
    return jsonify({'status': 'deleted'})

@app.route('/discussion', methods=['GET', 'POST'])
def discussion():
    return render_template('discussion.html')
#----------------------------------------------------------------#

@app.route('/dropdowns')
def dropdowns():
    return render_template('/just-features/dropdowns.html')

#----------------------------------------------------------------#

class User(UserMixin):
    def __init__(self, user_id):
        user_data = database.get_user(user_id)
        if user_data is not None:
            self.id = user_id
            self.username = user_data[5]
            self.is_admin = user_data[7]
               

@login_manager.user_loader
def load_user(user_id):
    user_data = database.get_user(user_id)
    if user_data is not None:
        return User(user_data[0])
    # Если user_id некорректный, то нужно вернуть None
    return None

@app.route('/')
@app.route('/home')
def home():
    logged_in = current_user.is_authenticated  # Автоматическая проверка статуса
    if logged_in:
        admin = current_user.is_admin
    else:
        admin = False
    return render_template('home.html', loggedIn=logged_in, admin = admin)

@app.route('/tasks')
def tasks():
    logged_in = current_user.is_authenticated  # Автоматическая проверка статуса
    return render_template('tasks.html', loggedIn=logged_in)



@app.route('/account')
def account():
    logged_in = current_user.is_authenticated
    if not logged_in:
        return render_template('not_logged.html') #ДОДЕЛАТЬ
    user = database.get_user(current_user.id)
    achievements = database.get_user_achievements(current_user.id)
    return render_template('account.html', user=user, loggedIn=logged_in, achievements=achievements)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/courses')
def courses():
    logged_in = current_user.is_authenticated  # Автоматическая проверка статуса
    if logged_in:
        admin = current_user.is_admin
    else:
        admin = False
    return render_template('courses.html', loggedIn=logged_in, admin=admin)

@app.route('/register', methods=['GET', 'POST'])
def register():
    logged_in = current_user.is_authenticated
    if logged_in:
        return 1
    if request.method == 'GET':
        return render_template("register.html", loggedIn=logged_in)
    elif request.method == 'POST':
        data = dict(request.form)
        print(data)
        database.add_user(data)
        user_data = database.login_user(data['username'])
        user = User(user_data[0])
        login_user(user)
        database.add_user_achiev(current_user.id, 'start')
        return render_template("home.html", loggedIn = True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_in = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('login.html',loggedIn=logged_in)
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = database.login_user(username)
        if user_data and user_data[1] == password:
            user = User(user_data[0])
            login_user(user)
            return redirect(url_for('home'))
        
        return 'Неверные данные! <a href="/login">Попробовать снова</a>'



@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    logged_in = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('add_course.html', loggedIn=logged_in)
    elif request.method == 'POST':
        data = request.form.getlist('subjects')
        user_id = current_user.id
        print(data)
        #database.add_course(data, user_id)
        return 'Курс создан!'
    


#=================================================================================================

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")