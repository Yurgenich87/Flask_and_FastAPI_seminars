from flask import Flask, render_template

app = Flask(__name__)


@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clothing')
def clothing():
    category = {
        'title': 'Clothing',
        'products': [
            {'id': 1, 'name': 'T-shirt', 'price': 20, 'image': 'tshirt.png'},
            {'id': 2, 'name': 'Jeans', 'price': 50, 'image': 'jeans.png'}
        ]
    }
    return render_template('category.html', category=category)


@app.route('/shoes')
def shoes():
    category = {
        'title': 'Shoes',
        'products': [
            {'id': 3, 'name': 'Sneakers', 'price': 70, 'image': 'sneakers.png'},
            {'id': 4, 'name': 'Boots', 'price': 100, 'image': 'boots.png'}
        ]
    }
    return render_template('category.html', category=category)


@app.route('/products/<int:product_id>')
def product(product_id):
    product = {
        'id': product_id,
        'name': 'Sample Product',
        'price': 50,
        'description': 'This is a sample product.',
        'image': 'image/sample_product.png'  # Путь к изображению товара
    }
    return render_template('product.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
