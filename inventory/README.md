# INSTALLATION

| packages | Usage                     |
| -------- | ------------------------- | 
|fastapi   | API development framework |  
|uvicorn   | Server to host api        | 
|redis-om  | Database, Message queue   |

```
# pip3 install fastapi "uvicorn[standard]" redis-om
```

# MICROSERVICE - 1 : Inventory

## Features

1. Keep tracks of the products.

2. CRUD operations are done to create, read, update, delete the product.

## Working

This microservice can be used by warehouse/sellers to keep track of their items. 

For routes please run the program and check http://localhost:8000/docs 

Redis-Stream is used for message queuing. Another microservice "payment" get the orders from the customers and puts to the Redis-Stream.

"inventory" microservice picks up those messages/events at 1 event/sec and does the processing(ie., updates the quantity_available after succesfull purchase)

## RUN 

Run main program in Console 1

```
# python3 main.py 

```

Run consumer on another console

```
# python3 consumer.py
```