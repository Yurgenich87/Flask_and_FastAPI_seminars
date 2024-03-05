from pathlib import PurePath, Path
from flask import Flask, url_for, request, render_template, abort, redirect, flash, session
from werkzeug.utils import secure_filename
from Lesson.lesson_2.templates.db import get_blog


app = Flask(__name__)
app.secret_key = b'f2dc28d9fc71a0524b9ffbbef079e01600cb2abc957692d03d6db4b7fc5a24f3'


@app.route('/')
def index():
    """Главная страница"""
    if 'username' in session:
        return f'Привет, {session["username"]}'
    else:
        return redirect(url_for('login'))
    # context = {
    #     'title': 'Обо мне',
    #     'name': 'Юрий',
    # }
    # # Устанавливаем cookie
    # response = make_response(render_template('main.html', **context))
    # response.headers['new_head'] = 'New-value'
    # response.set_cookie('username', context['name'])
    # return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Регистрайия на сайте"""
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        return redirect(url_for('index'))
    return render_template('username_form.html')


@app.route('/logout')
def logout():
    """Выход с сайта"""
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/getcookie/')
def get_cookies():
    """Получаем значение cookie"""
    name = request.cookies.get('username')
    return f'Значение cookie: {name}'


@app.route('/index/')
def html_index():
    """Страница обо мне"""
    context = {
        'title': 'Обо мне',
        'name': 'Юрий',
    }
    return render_template('index.html', **context)


@app.route('/redirect/')
def redirect_to_index():
    """Перенаправление на главную страницу """
    return redirect(url_for('index'))


@app.route('/external/')
def external_redirect():
    """Редирект на сайт"""
    return redirect('https://www.python.org/')


@app.route('/hello/<name>')
def hello(name):
    """Приветствие при вводе имени"""
    return f'Привет, {name}!'


@app.route('/redirect/<name>')
def redirect_to_hello(name):
    return redirect(url_for('hello', name=name))


@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('new_main.html', **context)


@app.route('/data/')
def data():
    context = {'title': 'База статей'}
    return render_template('new_data.html', **context)


@app.route('/about/')
def about():
    context = {
        'title': 'Обо мне',
        'name': 'Юрий',
    }
    return render_template('about.html', **context)


# @app.route('/<path:file>/')
# def get_file(file):
#     print(file)
#     return f'Ваш файл находится в: {escape(file)}'  # Экранирование строк


@app.route('/get/')
def get():
    if level := request.args.get('level'):
        text = f'Похоже ты опытный игрок, раз имеешь уровень {level}<br>'
    else:
        text = 'Привет новичек.<br>'
    return f'{text} {request.args}'


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        return f'Hello {name}'
    return render_template('form.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f'Файл {file_name} загружен на сервер'
    return render_template('upload.html')


@app.route('/1test_url_for/<int:num>/')
def a_test_url(num):
    text = f'В num лежит {num}<br>'
    text += f'Функция {url_for("a_test_url", num=42) = }<br>'
    text += f'Функция {url_for("a_test_url", num=42, data="new_data") = }<br>'
    text += f'Функция {url_for("a_test_url", num=42, data="new_data", pi=3.14515) = }<br>'
    return text


@app.route('/if/')
def show_if():
    context = {
        'title': 'Обо мне',
        'user': 'Крутой хакер',
        'name': 'Юрий',
        'number': 3,
    }
    return render_template('show_if.html', **context)


@app.route('/users/')
def users():
    _users = [{'name': 'Vladimir',
               'mail': 'vladimir@mail.ru',
               'phone': '+7-954-999-64-25'},
              {'name': 'Ivan',
               'mail': 'ivan@mail.ru',
               'phone': '+7-944-956-66-77'},
              {'name': 'Maksim',
               'mail': 'maksim@mail.ru',
               'phone': '+7-555-966-88-00'}
                ]
    context = {
        'users': _users,
        'title': 'Точечная нотация',
    }
    return render_template('users.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url,
    }
    return render_template('404.html', **context), 404


@app.errorhandler(500)
def page_not_found(e):
    app.logger.error(e)
    context = {
        'title': 'Ошибка сервера',
        'url': request.base_url,
    }
    return render_template('500.html', **context), 500


@app.route('/blog/<int:id>')
def get_blog_by_id(id):
    ...
    # Делаем запрос в БД для поиска статьи по id
    result = get_blog(id)
    if result is None:
        abort(404)
    ...
    # Возвращаем найденую в БД статью


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Обработка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        # Обработка данных формы
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('flash_form.html')


if __name__ == '__main__':
    app.run(debug=True)
