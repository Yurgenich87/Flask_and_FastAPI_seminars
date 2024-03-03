import secrets
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Home_work.models import db_users, User, Post, Comment
from flask_wtf import FlaskForm, CSRFProtect

from forms import LoginForm, RegistrationForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/shop.db'
db_users.init_app(app)
target_metadata = db_users.metadata

"""
Генерация надежного секретного ключа
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SECRET_KEY'] = b'487fd588d63ce2c6196ee322af441c437394ce68beebb442c91228bdc69ad67b'

csrf = CSRFProtect(app)

# Название интернет-магазина
app.config['STORE'] = '"Краски стиля"'


def add_user(username, email, password):
    """Добавление пользователя"""
    user = User(username=username, email=email, password=password)
    db_users.session.add(user)
    db_users.session.commit()
    print('Пользователь добавлен в базу данных!')


@app.cli.command("init-db")
def init_db():
    """Создание базы данных"""
    db_users.create_all()
    print('OK')


# @app.cli.command("edit-user")
def edit_user(username, new_email):
    """Редактирование пользователя"""
    user = User.query.filter_by(username=username).first()
    user.email = new_email
    db_users.session.commit()
    print('Edit John mail in DB!')


# @app.cli.command("del-user")
def delete_user(username):
    """Удаление пользователя"""
    user = User.query.filter_by(username=username).first()
    db_users.session.delete(user)
    db_users.session.commit()


@app.route('/form/', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return 'No CSRF protection'


@app.route('/', methods=['GET', 'POST'])
def main():
    tab = app.config['STORE']
    title = 'Главная'
    context = ''
    category = None

    return render_template('base.html', category=category, tab=tab, title=title)


@app.route('/index/', methods=['GET', 'POST'])
def index():
    """Главная"""
    tab = app.config['STORE']
    title = 'Главная'
    category = None
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('index.html', category=category, tab=tab, title=title)


@app.route('/data/')
def data():
    return 'Your data'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Вход"""
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Вход'
    context = 'Вход'
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Получение данных из формы
        username = form.username.data
        password = form.password.data

        # Проверка аутентификации пользователя
        if authenticate_user(username, password):
            # Пользователь аутентифицирован, перенаправляем на главную страницу
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))

    return render_template('login.html', category=category, tab=tab + title, title=title, context=context, form=form)


def authenticate_user(username, password):
    """Аутентификация пользователя"""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Пользователь найден и пароль совпадает
        return True
    else:
        # Пользователь не найден или пароль неверен
        return False


@app.route('/register/', methods=['GET', 'POST'])
def register():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Регистрация'
    context = 'Зарегистрироваться'
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        add_user(username, email, password)

        return redirect(url_for('index'))
    return render_template('register.html', category=category, tab=tab + title,
                           title=title, context=context, form=form)


@app.route('/logout/')
def logout():
    """Выход из системы"""
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/services/')
def services():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Сервисы'

    return render_template('services.html', category=category, tab=tab, title=title)


@app.route('/contacts/')
def contacts():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Контакты'

    return render_template('contacts.html', category=category, tab=tab, title=title)



@app.route('/product/')
def product():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Товары'
    products = [
        {'name': 'Футболка', 'price': 20, 'image': 'tshirt.png', 'category': 'Одежда'},
        {'name': 'Джинсы', 'price': 50, 'image': 'jeans.png', 'category': 'Одежда'},
        {'name': 'Кофта', 'price': 30, 'image': 'sweater.png', 'category': 'Одежда'},
        {'name': 'Платье', 'price': 60, 'image': 'dress.png', 'category': 'Одежда'},

    ]
    return render_template('product.html', category=category, tab=tab, title=title, products=products)


if __name__ == '__main__':
    app.run(debug=True)
