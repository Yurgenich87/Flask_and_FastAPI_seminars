import secrets
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Home_work.models import db_users, User, Product, CartItem, Order
from flask_wtf import FlaskForm, CSRFProtect
from data_base import clothing_products
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['WTF_CSRF_ENABLED'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Yurgenich/Desktop/PYTHON/Flask_and_FastAPI_seminars/instance/shop.db'
db_users.init_app(app)
target_metadata = db_users.metadata


# Создаем таблицы
with app.app_context():
    db_users.create_all()

"""
Генерация надежного секретного ключа
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SECRET_KEY'] = b'487fd588d63ce2c6196ee322af441c437394ce68beebb442c91228bdc69ad67b'


# Название интернет-магазина
app.config['STORE'] = '"Краски стиля"'


# @app.cli.command("init-db")
def init_db():
    """Создание базы данных"""
    db_users.create_all()
    print('OK')


@app.route('/', methods=['GET', 'POST'])
def main():
    tab = app.config['STORE']
    title = 'Главная'
    context = ''
    category = None

    return render_template('base.html', category=category, tab=tab, title=title, total_price=get_total_price())


@app.route('/index/', methods=['GET', 'POST'])
def index():
    """Главная"""
    tab = app.config['STORE']
    title = 'Главная'
    category = None

    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('index.html', category=category, tab=tab, title=title, total_price=get_total_price())


@app.route('/form/', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return 'No CSRF protection'


@app.route('/data/')
def data():
    return 'Your data'


# _________________________________________________Users_____________________________________________________

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Вход"""
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Вход'
    context = 'Вход'
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        if authenticate_user(username, password):
            session['username'] = username

            user = User.query.filter_by(username=username).first()
            if user:
                user.is_logged_in = True
                db_users.session.commit()

            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))

    return render_template('login.html', category=category, tab=tab + title, title=title, context=context, form=form)


def authenticate_user(username, password):
    """Аутентификация пользователя"""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    else:
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
        first_name = form.first_name.data
        second_name = form.first_name.data
        email = form.email.data
        password = form.password.data

        add_user(username, first_name, second_name, email, password)

        return redirect(url_for('index'))
    return render_template('register.html', category=category, tab=tab + title,
                           title=title, context=context, form=form)


@app.route('/logout/')
def logout():
    """Выход из системы"""
    username = session.get('username')

    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_logged_in = False
            db_users.session.commit()

    session.pop('username', None)

    return redirect(url_for('login'))


@app.route('/services/')
def services():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Сервисы'

    return render_template('services.html', category=category, tab=tab, title=title, total_price=get_total_price())


@app.route('/contacts/')
def contacts():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Контакты'

    return render_template('contacts.html', category=category, tab=tab, title=title, total_price=get_total_price())


# @app.cli.command("add-user")
def add_user(username, first_name, last_name, email, password):
    """Добавление пользователя"""
    user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    db_users.session.add(user)
    db_users.session.commit()
    print('Пользователь добавлен в базу данных!')


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


def get_user_id():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id
    return user_id


def get_total_price():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return user.total_price
    else:
        return 0


# _________________________________________________Cart_____________________________________________________
@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Корзина'
    if not get_user_id():
        return redirect(url_for('login'))

    if request.method == 'POST':
        cart_id = request.form.get('cart_id')
        product_id = request.form.get('product_id')

        cart_item = CartItem.query.get(cart_id)
        db_users.session.delete(cart_item)

        order = Order(user_id=get_user_id(), product_id=product_id)
        db_users.session.add(order)

        db_users.session.commit()
        return redirect(url_for('cart'))  # Перенаправляем обратно на страницу корзины

    cart_items = CartItem.query.filter_by(user_id=get_user_id(), status='active').all()
    if not cart_items:
        return render_template('cart.html', category=category, tab=tab, title=title, products=0, total_price=0)

    products = []

    for cart_item in cart_items:
        product = cart_item.product
        products.append({'cart_id': cart_item.cart_id, 'name': product.product_name, 'price': product.price,
                         'quantity': cart_item.quantity})

    return render_template('cart.html', category=category, tab=tab, title=title,
                           products=products, total_price=get_total_price())


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if not get_user_id():
        return redirect(url_for('login'))

    cart_item = CartItem(user_id=get_user_id(), product_id=product_id, quantity=1)
    db_users.session.add(cart_item)
    db_users.session.commit()

    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    user.update_total_price()

    return redirect(url_for('product'))


@app.route('/create_order/')
def create_order():

    if not get_user_id():
        return redirect(url_for('login'))

    cart_item = CartItem.query.filter_by(cart_id=1, status='active').all()
    product_id = cart_item.product_id

    order = Order(user_id=get_user_id(), product_id=product_id)

    db_users.session.delete(cart_item)
    db_users.session.add(order)

    db_users.session.commit()

    user = User.query.get(get_user_id())
    user.update_total_price()

    return redirect(url_for('cart'))


# _________________________________________________Product_____________________________________________________
@app.route('/product/', methods=['GET', 'POST'])
def product():
    tab = app.config['STORE']
    title = 'Главная'
    category = 'Товары'

    products = Product.query.all()

    return render_template('product.html', category=category, tab=tab, title=title,
                           products=products, total_price=get_total_price())


@app.cli.command("add-products")
def add_products_to_database():
    for product_data in clothing_products:
        new_product = Product(product_name=product_data['name'], price=product_data['price'], content=product_data['content'],
                              image=product_data['image'], category=product_data['category'])
        db_users.session.add(new_product)

    db_users.session.commit()


if __name__ == '__main__':
    app.run(debug=True)

