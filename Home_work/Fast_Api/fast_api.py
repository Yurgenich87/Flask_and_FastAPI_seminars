from datetime import datetime
from typing import List, Optional, Annotated
import databases
import ormar
import sqlalchemy
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import create_engine, ForeignKey, select, column, delete, update

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(100)),

)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("product_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String(32)),
    sqlalchemy.Column("price", sqlalchemy.Float(10000)),
    sqlalchemy.Column("content", sqlalchemy.String(1000)),
    )

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("users.user_id"), nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, ForeignKey("products.product_id"), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float(10000), ForeignKey("products.price"), nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(False)),
    sqlalchemy.Column("status", sqlalchemy.Boolean(False)),

)


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


# _____________________________________________________User__________________________________________________________
class UserIn(BaseModel):
    first_name: str = Field(max_length=128)
    last_name: str = Field(max_length=128)
    email: EmailStr
    password: str = Field(max_length=50)


class User(BaseModel):
    user_id: int
    first_name: str = Field(max_length=128)
    last_name: str = Field(max_length=128)
    email: EmailStr
    password: str = Field(max_length=50)


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                  password=user.password)
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "user_id": last_record_id}


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.user_id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "user_id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# _____________________________________________________Product__________________________________________________________
class ProductIn(BaseModel):
    product_name: str = Field(max_length=200)
    content: str = Field(max_length=1000)
    price: float


class Product(BaseModel):
    product_id: int
    product_name: str = Field(max_length=200)
    content: str = Field(max_length=1000)
    price: float


@app.get("/products/", response_model=List[Product])
async def read_users():
    query = products.select()
    return await database.fetch_all(query)


@app.post("/product/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(product_name=product.product_name, price=product.price, content=product.content)
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "product_id": last_record_id}


@app.get("/product/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.product_id == product_id)
    return await database.fetch_one(query)


@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.product_id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "product_id": product_id}


@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.product_id == product_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# _____________________________________________________Order__________________________________________________________

class OrderIn(BaseModel):
    user_id: int
    product_id: int


class Order(OrderIn):
    order_id: int
    price: float
    created_at: datetime
    status: bool


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = select([orders])
    return await database.fetch_all(query)


@app.post("/order/", response_model=Order)
async def create_order(order: OrderIn):
    price_query = select([products.c.price]).where(products.c.product_id == order.product_id)
    price = await database.fetch_val(price_query)

    user_query = select([users.c.user_id]).where(users.c.user_id == order.user_id)
    user_id = await database.fetch_val(user_query)

    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        price=price,
        created_at=datetime.now(),
        status=True
    )
    last_record_id = await database.execute(query)

    return {
        "order_id": last_record_id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "price": price,
        "created_at": datetime.now(),
        "status": True
    }


@app.get("/order/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = select([orders]).where(orders.c.order_id == order_id)
    return await database.fetch_one(query)


@app.put("/order/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = update(orders).where(orders.c.order_id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "order_id": order_id}


@app.delete("/order/{order_id}")
async def delete_order(order_id: int):
    query = delete(orders).where(orders.c.order_id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
