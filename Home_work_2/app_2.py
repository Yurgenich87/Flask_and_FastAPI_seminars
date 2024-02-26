from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)


@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    title = 'Магазин "Краски стиля"'
    category = None
    return render_template('index.html', title=title, category=category)


@app.route('/clothing')
def clothing():
    category_clothing = {
        'title': 'Одежда',
        'products': [
            {'id': 1, 'name': 'Футболка', 'price': 20, 'image': 'tshirt.png'},
            {'id': 2, 'name': 'Джинсы', 'price': 50, 'image': 'jeans.png'},
            {'id': 3, 'name': 'Кофта', 'price': 30, 'image': 'sweater.png'},
            {'id': 4, 'name': 'Платье', 'price': 60, 'image': 'dress.png'},
            {'id': 5, 'name': 'Пиджак', 'price': 70, 'image': 'blazer.png'},
            {'id': 6, 'name': 'Юбка', 'price': 40, 'image': 'skirt.png'},
            {'id': 7, 'name': 'Рубашка', 'price': 35, 'image': 'shirt.png'},
            {'id': 8, 'name': 'Пальто', 'price': 80, 'image': 'coat.png'},
            {'id': 9, 'name': 'Брюки', 'price': 45, 'image': 'pants.png'},
            {'id': 10, 'name': 'Шорты', 'price': 25, 'image': 'shorts.png'}
        ]
    }
    return render_template('category.html', category=category_clothing, title=category_clothing['title'])


@app.route('/shoes')
def shoes():
    category_shoes = {
        'title': 'Обувь',
        'products': [
            {'id': 11, 'name': 'Кросовки', 'price': 70, 'image': 'sneakers.png'},
            {'id': 12, 'name': 'Сапоги', 'price': 100, 'image': 'boots.png'},
            {'id': 13, 'name': 'Туфли на каблуке', 'price': 90, 'image': 'heels.png'},
            {'id': 14, 'name': 'Мокасины', 'price': 60, 'image': 'moccasins.png'},
            {'id': 15, 'name': 'Ботфорты', 'price': 110, 'image': 'high_boots.png'},
            {'id': 16, 'name': 'Балетки', 'price': 45, 'image': 'ballet_flats.png'},
            {'id': 17, 'name': 'Сандалии', 'price': 80, 'image': 'sandals.png'},
            {'id': 18, 'name': 'Лоферы', 'price': 55, 'image': 'loafers.png'},
            {'id': 19, 'name': 'Эспадрильи', 'price': 75, 'image': 'espadrilles.png'},
            {'id': 20, 'name': 'Полуботинки', 'price': 85, 'image': 'oxfords.png'}
        ]
    }
    return render_template('category.html', category=category_shoes, title=category_shoes['title'])


# @app.route('/products/<int:product_id>')
# def product(product_id):
#     # Логика для получения информации о товаре по его ID
#     product = get_product_by_id(product_id)
#     return render_template('product.html', product=product)
#

if __name__ == '__main__':
    app.run(debug=True)
