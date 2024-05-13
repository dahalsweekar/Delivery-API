from pydantic import BaseModel


class SignUpModel(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str
    is_staff: bool | None = None
    is_active: bool | None = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            'example': {
                "username": "john",
                "email": "john@gmail.com",
                "password": "**********",
                "is_staff": False,
                "is_active": False
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '5cb2cd944cb4934bc303698e6433964e1f62ab2cbba773109f6626ae478cc839'


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: int | None = None
    quantity: int
    order_status: str | None = "PENDING"
    pizza_size: str | None = "SMALL"
    user_id: int | None = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "quantity": 100,
                "pizza_size": "LARGE"
            }
        }


class OrderStatusModel(BaseModel):
    order_status: str | None = "PENDING"

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }
