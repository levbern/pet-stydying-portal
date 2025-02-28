from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Здесь вы можете добавить логику аутентификации
        flash(f'Welcome, {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('flask-wtf.html', form=form)

@app.route('/home')
def home():
    return "Welcome to the home page!"

if __name__ == '__main__':
    app.run(debug=True)
