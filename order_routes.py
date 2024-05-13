from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = SessionLocal(bind=engine)


@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):

    """
        ## A sample hello world route
        This returns hello world
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')
    return {"message": "Hello World"}


@order_router.post('/order', status_code=201)
async def place_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    """
            ## Placing an Order
            This requires the following
            - Quantity: integer
            - Pizza Size: String
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.pizza_size,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(status_code=401, detail="Unauthorized request")


@order_router.get('/orders/{id}')
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        db_order = session.query(Order).filter(Order.id == id).first()
        return jsonable_encoder(db_order)

    raise HTTPException(status_code=401, detail="Unauthorized request")


@order_router.get('/users/orders')
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('user/order/{id}/')
async def get_specific_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    orders = current_user.orders
    for o in orders:
        if o.id == id:
            return orders

    raise HTTPException(status_code=400, detail="No order with such id")


@order_router.put('/order/update/{id}/')
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    order_to_update = session.query(Order).filter(Order.id == id).first()

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status,
    }

    session.add(order_to_update)
    session.commit()

    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}')
async def update_order_status(id: int, order: OrderStatusModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).filter()

    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()
        order_to_update.order_status = order.order_status

        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status,
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=404, detail="Unauthorized request")


@order_router.delete('/order/delete/{id}/', status_code=204)
async def delete_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_order = session.query(Order).filter(Order.id == id).first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    session.delete(db_order)
    session.commit()

    return "success"
