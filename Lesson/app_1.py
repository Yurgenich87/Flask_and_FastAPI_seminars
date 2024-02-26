from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hi'


@app.route('/index/')
def html_index():
    context = {
        'title': 'Обо мне',
        'name': 'Харитон',
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run()
