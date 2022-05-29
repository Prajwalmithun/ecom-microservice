from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel
from requests import request


# to read value defined in .env file
load_dotenv()

app = FastAPI()

# add middleware to fix UI - Backend port mismatch
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


# Redis configuration
REDIS_DATABASE_NAME = os.getenv("REDIS_DATABASE_NAME")
REDIS_ENDPOINT = os.getenv("REDIS_ENDPOINT")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# connecting to redis
redis = get_redis_connection(
    host=REDIS_ENDPOINT,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# our model
class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    # actual redis connection
    class Meta:
        database = redis


# this method to get all the products
@app.get("/")
def allProduct():
    return [format(pk) for pk in Product.all_pks()]

# this is a helper method, just to return the products details
def format(pk: str):
    product = Product.get(pk)

    return{
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity_available

        }

# this method is for adding products to the DB
@app.post('/products')
def createProduct(product: Product):
    return product.save()

# method to get inndividual product
@app.get("/products/{pk}")
def getSpecificProduct(pk: str):
    return Product.get(pk)

# delete the product from the inventory
@app.delete("/products/{pk}")
def deleteProduct(pk: str):
    return Product.delete(pk)

# update the product details
@app.put("/products/update/{pk}")
def updateProduct(pk: str):
    prodObj = Product.get(pk)

    body = request.json()

    prodObj['name'] = body['name']
    prodObj['price'] = body['price']
    prodObj['quantity_available'] =  prodObj['quantity_available'] + body['new_quantity']

    return prodObj.save()

# @app.get("/")
# def read_root():
#     return {"Hello":"world"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}