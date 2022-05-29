from main import redis, Product 
import time

key = 'order_completed'
group = 'inventory_group'

# Creating redis group
try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists!")

# Reading messages/events from Redis stream
while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        #print(results)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj['productID'])
                print(obj)
                print(obj['quantity_purchase'])
                product.quantity_available = product.quantity_available - int(obj['quantity_purchase'])
                product.save()

    except Exception as e:
        print(str(e))

    time.sleep(1)