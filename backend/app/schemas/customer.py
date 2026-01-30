# backend/app/schemas/customer.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "USA"

class CustomerCreate(CustomerBase):
    date_of_birth: Optional[datetime] = None
    ssn_last_4: Optional[str] = None
    
    @validator('ssn_last_4')
    def validate_ssn(cls, v):
        if v and (len(v) != 4 or not v.isdigit()):
            raise ValueError('SSN last 4 must be 4 digits')
        return v

class CustomerUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    status: Optional[str] = None

class Customer(CustomerBase):
    id: int
    customer_since: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Updated from orm_mode