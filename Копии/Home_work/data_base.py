from app_main import db_users, Product, app


@app.route('/add_products_to_database')
def add_products_to_database():
    products = [
        {'name': 'Футболка', 'price': 20, 'image': 'tshirt.png', 'category': 'Одежда'},
        {'name': 'Джинсы', 'price': 50, 'image': 'jeans.png', 'category': 'Одежда'},
        {'name': 'Кофта', 'price': 30, 'image': 'sweater.png', 'category': 'Одежда'},
        {'name': 'Платье', 'price': 60, 'image': 'dress.png', 'category': 'Одежда'},
        {'name': 'Пиджак', 'price': 70, 'image': 'blazer.png', 'category': 'Одежда'},
        {'name': 'Юбка', 'price': 40, 'image': 'skirt.png', 'category': 'Одежда'},
        {'name': 'Рубашка', 'price': 35, 'image': 'shirt.png', 'category': 'Одежда'},
        {'name': 'Пальто', 'price': 80, 'image': 'coat.png', 'category': 'Одежда'},
        {'name': 'Брюки', 'price': 45, 'image': 'pants.png', 'category': 'Одежда'},
        {'name': 'Шорты', 'price': 25, 'image': 'shorts.png', 'category': 'Одежда'},
        {'name': 'Кросовки', 'price': 70, 'image': 'sneakers.png', 'category': 'Обувь'},
        {'name': 'Сапоги', 'price': 100, 'image': 'boots.png', 'category': 'Обувь'},
        {'name': 'Туфли на каблуке', 'price': 90, 'image': 'heels.png', 'category': 'Обувь'},
        {'name': 'Мокасины', 'price': 60, 'image': 'moccasins.png', 'category': 'Обувь'},
        {'name': 'Ботфорты', 'price': 110, 'image': 'high_boots.png', 'category': 'Обувь'},
        {'name': 'Балетки', 'price': 45, 'image': 'ballet_flats.png', 'category': 'Обувь'},
        {'name': 'Сандалии', 'price': 80, 'image': 'sandals.png', 'category': 'Обувь'},
        {'name': 'Лоферы', 'price': 55, 'image': 'loafers.png', 'category': 'Обувь'},
        {'name': 'Эспадрильи', 'price': 75, 'image': 'espadrilles.png', 'category': 'Обувь'},
        {'name': 'Полуботинки', 'price': 85, 'image': 'oxfords.png', 'category': 'Обувь'}
    ]

    for product_data in products:
        product = Product(
            name=product_data['name'],
            price=product_data['price'],
            image=product_data['image'],
            category=product_data['category']
        )
        db_users.session.add(product)

    db_users.session.commit()

    return 'Products added to database successfully!'

