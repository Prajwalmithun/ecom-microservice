from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
import os
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

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
# Ideally payment microservice should have different db.
# Best practise: 1 microservice = 1 DB
redis = get_redis_connection(
    host=REDIS_ENDPOINT,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# our model
class Order(HashModel):
    productID: str
    price: float
    fee: float
    total: float
    quantity_purchase: int
    status: str # pending,success,refunded


    # actual redis connection
    class Meta:
        database = redis

# get the order
# just to test the "status"
@app.get("/orders/{pk}")
def getOrder(pk: str):
    return Order.get(pk)


# ordering the product
@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks): #parameters = id, quantity
    body = await request.json()

    # get the product's info from invetory microservice
    req = requests.get('http://localhost:8000/products/%s' % body['id'])

    product = req.json()

    # parsing the product object
    order = Order(
        productID = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity_purchase = body['quantity_purchase'],
        status = 'pending'
    )

    # adding to redis db
    order.save()

    # for making delay effective because we are using async functions
    background_tasks.add_task(order_completed, order)

    #order_completed(order)
    return order 

# This method is for handling status of the order
def order_completed(order: Order):
    # adding 5sec delay for payment processing
    time.sleep(5)
    order.status = 'success'
    order.save()

    # updating the quantity_available after the purchase using Redis Stream
    redis.xadd('order_completed',order.dict(), '*')