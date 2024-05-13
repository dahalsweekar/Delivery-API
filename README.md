# Introduction
This is a REST API for a delivery service built using FastAPI, SQLAlchemy and SQLITE.

# Routes

| Method  | Route | Functions | Access |
| ------------- | ------------- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | *Register new user* | *All users* |
| *POST* | ```/auth/login/``` | *Login user* | *All users* |
| *POST* | ```/orders/order/``` | *Place an order* | *All users* |
| *PUT* | ```/orders/order/update/{order_id}/``` | *Update an order* | *All users* |
| *PUT* | ```/orders/order/status/{order_id}/``` | *Update order status* | *Superusers* |
| *DELETE* | ```/orders/order/delete/{order_id}/``` | *Delete/Remove an order* | *All users* |
| *GET* | ```/orders/user/orders/``` | *Get user's orders* | *All users* |
| *GET* | ```/orders/orders/``` | *List all orders made* | *Superusers* |
| *GET* | ```/orders/orders/{order_id}/``` | *Retrieve an order* | *Superusers* |
| *GET* | ```/orders/user/orders/{order_id}/``` | *Get user's specific order* |  |
| *GET* | ```/docs/``` | *View API documentation* | *All users* |
