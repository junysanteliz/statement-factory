# backend/app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from app.crud import customer_crud

router = APIRouter()

@router.get("/", response_model=List[Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve customers with optional filtering
    """
    customers = customer_crud.get_customers(
        db, skip=skip, limit=limit, search=search, status=status
    )
    return customers

@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a specific customer by ID
    """
    db_customer = customer_crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer
    """
    # Check if customer with email already exists
    db_customer = db.query(customer_crud.Customer).filter(
        customer_crud.Customer.email == customer.email
    ).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return customer_crud.create_customer(db=db, customer=customer)

@router.put("/{customer_id}", response_model=Customer)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a customer
    """
    db_customer = customer_crud.update_customer(db, customer_id, customer_update)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer
    """
    success = customer_crud.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.get("/{customer_id}/loans")
def get_customer_loans(customer_id: int, db: Session = Depends(get_db)):
    """
    Get all loans for a customer
    """
    from app.crud import loan_crud
    loans = loan_crud.get_loans_by_customer(db, customer_id)
    return loans