import secrets
from flask import Flask, render_template, request, session, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = secrets.token_hex(16)
target_metadata = db.metadata


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)


# Определение модели пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()

app.config['STORE'] = '"Краски стиля"'


@app.route('/', methods=['GET', 'POST'])
def main():
    tab = app.config['STORE']
    title = 'Главная'
    context = ''
    category = None

    return render_template('base.html', category=category, tab=tab, title=title)


@app.route('/login/')
def login():
    tab = app.config['STORE']
    title = 'Главная'
    context = 'Вход'
    category = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html', category=category, tab=tab+title, title=title, context=context)


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
