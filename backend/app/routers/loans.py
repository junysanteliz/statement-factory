# backend/app/routers/loans.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.loan import Loan, LoanCreate, LoanUpdate
from app.crud import loan_crud, customer_crud

router = APIRouter()

@router.get("/", response_model=List[Loan])
def read_loans(
    skip: int = 0,
    limit: int = 100,
    loan_type: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve loans with optional filtering
    """
    loans = loan_crud.get_loans(
        db, skip=skip, limit=limit, 
        loan_type=loan_type, status=status, customer_id=customer_id
    )
    return loans

@router.get("/{loan_id}", response_model=Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    """
    Get a specific loan by ID
    """
    db_loan = loan_crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@router.post("/", response_model=Loan)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """
    Create a new loan
    """
    # Check if customer exists
    customer = customer_crud.get_customer(db, loan.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if loan account number already exists
    if loan.loan_account_number:
        existing_loan = loan_crud.get_loan_by_account_number(db, loan.loan_account_number)
        if existing_loan:
            raise HTTPException(status_code=400, detail="Loan account number already exists")
    
    return loan_crud.create_loan(db=db, loan=loan)

@router.put("/{loan_id}", response_model=Loan)
def update_loan(
    loan_id: int,
    loan_update: LoanUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a loan
    """
    db_loan = loan_crud.update_loan(db, loan_id, loan_update)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@router.get("/{loan_id}/summary")
def get_loan_summary(loan_id: int, db: Session = Depends(get_db)):
    """
    Get loan summary including calculated fields
    """
    summary = loan_crud.get_loan_summary(db, loan_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Loan not found")
    return summary