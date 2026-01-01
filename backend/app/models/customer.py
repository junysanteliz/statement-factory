from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: str
    name: str
    address: str
    phone: str
    email: str