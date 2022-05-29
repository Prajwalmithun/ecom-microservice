# INSTALLATION

| packages | Usage                     |
| -------- | ------------------------- | 
|fastapi   | API development framework |  
|uvicorn   | Server to host api        | 
|redis-om  | Database, Message queue   |
 

```
# pip3 install fastapi "uvicorn[standard]" redis-om
```

# MICROSERVICE - 2 : Payment

## Features

1. Book the orders by providing the product ID and quantity

## Working

This microservice takes productID and quantity as inputs. Making a GET request to "inventory" microservice to get the product details.

If the purchase goes well, "status": "success" will be shown.

Other status are "pending" and "refunded"