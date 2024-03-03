from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db_users = SQLAlchemy()


class User(db_users.Model):
    id = db_users.Column(db_users.Integer, primary_key=True)
    username = db_users.Column(db_users.String(80), unique=True, nullable=False)
    email = db_users.Column(db_users.String(120), unique=True, nullable=False)
    password = db_users.Column(db_users.String(100), nullable=False)
    created_at = db_users.Column(db_users.DateTime, default=datetime.utcnow)
    is_logged_in = db_users.Column(db_users.Boolean, default=False)
    last_login = db_users.Column(db_users.DateTime)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def login(self):
        self.is_logged_in = True
        self.last_login = datetime.utcnow()
        db_users.session.commit()

    def logout(self):
        self.is_logged_in = False
        db_users.session.commit()


class Post(db_users.Model):
    id = db_users.Column(db_users.Integer, primary_key=True)
    title = db_users.Column(db_users.String(80), nullable=False)
    content = db_users.Column(db_users.Text, nullable=False)
    author_id = db_users.Column(db_users.Integer, db_users.ForeignKey('user.id'), nullable=False)
    created_at = db_users.Column(db_users.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Post({self.title}, {self.content})'


class Comment(db_users.Model):
    id = db_users.Column(db_users.Integer, primary_key=True)
    content = db_users.Column(db_users.Text, nullable=False)
    post_id = db_users.Column(db_users.Integer, db_users.ForeignKey('post.id'), nullable=False)
    author_id = db_users.Column(db_users.Integer, db_users.ForeignKey('user.id'), nullable=False)
    created_at = db_users.Column(db_users.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Comment({self.content})'

# class Product(db.Model):
#     id_product = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String(50), nullable=False)


