from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pydantic import Field, BaseModel

db_users = SQLAlchemy()


# class User_P:
#     username: str = Field(..., title='Никнейм', max_length=80)
#     first_name: str = Field(..., title='Имя', max_length=80)
#     last_name: str = Field(..., title='Фамилия', max_length=80)
#     email: str = Field(..., title='email', max_length=120)
#     password: str = Field(..., title='Пароль', max_length=120)
#     created_at: datetime
#     is_logged_in: bool
#     last_login: datetime
#     total_price: float


class User(db_users.Model):
    user_id = db_users.Column(db_users.Integer, primary_key=True)
    username = db_users.Column(db_users.String(80), unique=True, nullable=False)
    first_name = db_users.Column(db_users.String(80), unique=True, nullable=False)
    last_name = db_users.Column(db_users.String(80), unique=True, nullable=False)
    email = db_users.Column(db_users.String(120), unique=True, nullable=False)
    password = db_users.Column(db_users.String(100), nullable=False)
    created_at = db_users.Column(db_users.DateTime, default=datetime.utcnow)
    is_logged_in = db_users.Column(db_users.Boolean, default=False)
    last_login = db_users.Column(db_users.DateTime)
    total_price = db_users.Column(db_users.Float, nullable=False, default=0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def login(self):
        self.is_logged_in = True
        self.last_login = datetime.utcnow()
        db_users.session.commit()

    def logout(self):
        self.is_logged_in = False
        self.last_login = datetime.utcnow()
        db_users.session.commit()

    def update_total_price(self):
        user = User.query.get(self.user_id)
        cart_items = CartItem.query.filter_by(user_id=self.user_id, status='active').all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        user.total_price = round(total_price, 2)
        db_users.session.commit()


# class Product_P(BaseModel):
#     product_name: str
#     price: float = Field(..., title='Цена', gt=0, le=100000)
#     content: str
#     image: str
#     category: str


class Product(db_users.Model):
    product_id = db_users.Column(db_users.Integer, primary_key=True)
    product_name = db_users.Column(db_users.String(100), nullable=False)
    price = db_users.Column(db_users.Float, nullable=False)
    content = db_users.Column(db_users.Text, nullable=False)
    image = db_users.Column(db_users.String(100), nullable=False)
    category = db_users.Column(db_users.String(50), nullable=False)

    def __repr__(self):
        return f'Product({self.title}, {self.content})'


# class Item_P(BaseModel):
#     name: str = Field(title="Name", max_length=50)
#     price: float = Field(title="Price", gt=0, le=100000)
#     description: str = Field(default=None, title="Description", max_length=1000)
#     tax: float = Field(0, title="Tax", ge=0, le=10)


class CartItem(db_users.Model):
    cart_id = db_users.Column(db_users.Integer, primary_key=True)
    user_id = db_users.Column(db_users.Integer, db_users.ForeignKey('user.user_id'), nullable=False)
    product_id = db_users.Column(db_users.Integer, db_users.ForeignKey('product.product_id'), nullable=False)
    quantity = db_users.Column(db_users.Integer, nullable=False, default=1)
    status = db_users.Column(db_users.String(20), nullable=False, default='active')
    created_at = db_users.Column(db_users.DateTime, default=datetime.utcnow)

    user = db_users.relationship('User', backref=db_users.backref('cart_items', lazy=True))
    product = db_users.relationship('Product', backref=db_users.backref('cart_items', lazy=True))

    def __repr__(self):
        return f'CartItem(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity}, status={self.status})'


class Order(db_users.Model):
    order_id = db_users.Column(db_users.Integer, primary_key=True)
    user_id = db_users.Column(db_users.Integer, db_users.ForeignKey('user.user_id'), nullable=False)
    product_id = db_users.Column(db_users.Integer, db_users.ForeignKey('product.product_id'), nullable=False)
    order_date = db_users.Column(db_users.DateTime, nullable=False, default=datetime.utcnow)
    status = db_users.Column(db_users.String(20), nullable=False, default='active')

    def __repr__(self):
        return f'Order(user_id={self.user_id}, product_id={self.product_id}, order_date={self.order_date}, status={self.status})'
