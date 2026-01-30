# backend/app/crud/loan_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models.loan import Loan
from app.models.customer import Customer
from app.schemas.loan import LoanCreate, LoanUpdate
import uuid
from datetime import datetime

def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.id == loan_id).first()

def get_loan_by_account_number(db: Session, account_number: str) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.loan_account_number == account_number).first()

def get_loans_by_customer(db: Session, customer_id: int) -> List[Loan]:
    return db.query(Loan).filter(Loan.customer_id == customer_id).all()

def get_loans(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    loan_type: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[int] = None
) -> List[Loan]:
    query = db.query(Loan)
    
    if loan_type:
        query = query.filter(Loan.loan_type == loan_type)
    
    if status:
        query = query.filter(Loan.loan_status == status)
    
    if customer_id:
        query = query.filter(Loan.customer_id == customer_id)
    
    return query.order_by(Loan.loan_account_number).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: LoanCreate) -> Loan:
    # Generate loan account number if not provided
    if not loan.loan_account_number:
        loan_type_prefix = {
            "personal": "PL",
            "mortgage": "MTG",
            "auto": "AL",
            "business": "BL",
            "education": "EL"
        }.get(loan.loan_type.lower(), "LN")
        loan.loan_account_number = f"{loan_type_prefix}{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
    
    # Initialize balances
    loan_data = loan.dict()
    loan_data["current_balance"] = loan.principal_amount
    loan_data["outstanding_principal"] = loan.principal_amount
    loan_data["outstanding_interest"] = 0.0
    
    db_loan = Loan(**loan_data)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(
    db: Session, 
    loan_id: int, 
    loan_update: LoanUpdate
) -> Optional[Loan]:
    db_loan = get_loan(db, loan_id)
    if db_loan:
        update_data = loan_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_loan, field, value)
        db.commit()
        db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int) -> bool:
    db_loan = get_loan(db, loan_id)
    if db_loan:
        db.delete(db_loan)
        db.commit()
        return True
    return False

def get_loan_summary(db: Session, loan_id: int) -> dict:
    loan = get_loan(db, loan_id)
    if not loan:
        return None
    
    # Calculate days to maturity
    from datetime import datetime
    days_to_maturity = (loan.maturity_date - datetime.utcnow()).days if loan.maturity_date else None
    
    return {
        "loan_account_number": loan.loan_account_number,
        "loan_type": loan.loan_type,
        "principal_amount": loan.principal_amount,
        "current_balance": loan.current_balance,
        "interest_rate": loan.interest_rate,
        "monthly_payment": loan.monthly_payment,
        "amount_due": loan.amount_due,
        "next_payment_date": loan.next_payment_date,
        "days_to_maturity": days_to_maturity,
        "loan_status": loan.loan_status
    }