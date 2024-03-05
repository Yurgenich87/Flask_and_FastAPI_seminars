from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.logger import logger

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def read_root():
    logger.info('Отработал GET запрос')
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.info('Отработал GET запрос')
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    logger.info('Отработал POST запрос')
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}.')
    return {"item_id": item_id, "item": item}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    logger.info(f'Отработал DELETE запрос для item id = {item_id}.')
    return {"item_id": item_id}
