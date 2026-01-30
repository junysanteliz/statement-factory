# backend/app/crud/customer_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models.customer2 import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
import uuid
from datetime import datetime

def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_by_external_id(db: Session, external_id: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.customer_id == external_id).first()

def get_customers(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None
) -> List[Customer]:
    query = db.query(Customer)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Customer.first_name.ilike(search_term),
                Customer.last_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.customer_id.ilike(search_term)
            )
        )
    
    if status:
        query = query.filter(Customer.status == status)
    
    return query.order_by(Customer.last_name, Customer.first_name).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    # Generate unique customer ID if not provided
    if not customer.customer_id:
        customer.customer_id = f"CUST{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
    
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(
    db: Session, 
    customer_id: int, 
    customer_update: CustomerUpdate
) -> Optional[Customer]:
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int) -> bool:
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return True
    return False

def get_customer_with_loans(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_count(db: Session) -> int:
    return db.query(Customer).count()