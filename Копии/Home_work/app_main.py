import secrets
from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Home_work.models import db_users, User, Post, Comment
from flask_wtf import FlaskForm, CSRFProtect

from forms import LoginForm

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


@app.cli.command("init-db")
def init_db():
    """Создание базы данных"""
    db_users.create_all()
    print('OK')


@app.cli.command("add-user")
def add_user():
    """Добавление пользователя"""
    user = User(username='john', email='john@example.com', password=123)
    db_users.session.add(user)
    db_users.session.commit()
    print('John add in DB!')


@app.cli.command("edit-user")
def edit_user():
    """Редактирование пользователя"""
    user = User.query.filter_by(username='john').first()
    user.email = 'new_email@example.com'
    db_users.session.commit()
    print('Edit John mail in DB!')


@app.cli.command("del-user")
def delete_user():
    """Удаление пользователя"""
    for i in range(1, 6):
        user = User.query.filter_by(username=f'user{i}').first()
        db_users.session.delete(user)
        db_users.session.commit()
        print('Delete John from DB!')


@app.cli.command("fill-db")
def fill_tables():
    count = 5
    for user in range(1, count + 1):
        new_user = User(username=f'user{user}', email=f'user{user}@gmail.com', password=1234)
        db_users.session.add(new_user)
    db_users.session.commit()

    for post in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{post % count + 1}').first()
        new_post = Post(title=f'Post title {post}', content=f'Post content {post}', author_id=author.id)
        db_users.session.add(new_post)
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


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


@app.route('/login/')
def login():
    tab = app.config['STORE']
    title = 'Главная'
    context = 'Вход'
    category = None

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', category=category, tab=tab+title, title=title, context=context, form=form)


# @app.route('/login/')
# def login():
#     tab = app.config['STORE']
#     title = 'Главная'
#     context = 'Вход'
#     category = None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             return 'Invalid username or password'
#     return render_template('login.html', category=category, tab=tab+title, title=title, context=context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    tab = app.config['STORE']
    title = 'Регистрация'
    context = 'Зарегистрироваться'
    category = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Проверяем, есть ли пользователь с таким email уже в базе
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Пользователь с таким email уже существует'

        # Хэшируем пароль перед сохранением
        hashed_password = generate_password_hash(password)

        # Создаем нового пользователя
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)

        # Добавляем нового пользователя в базу данных
        db_users.session.add(new_user)
        db_users.session.commit()

        session['email'] = email  # Может быть полезно для автоматического входа после регистрации
        return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу после успешной регистрации

    return render_template('register.html', category=category, tab=tab + title, title=title, context=context)




@app.route('/logout/')
def logout():
    """Выход из системы"""
    session.pop('username', None)
    return redirect(url_for('index'))


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
