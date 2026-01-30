# backend/app/schemas/loan.py
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class LoanBase(BaseModel):
    loan_account_number: str
    loan_type: str
    principal_amount: float
    interest_rate: float
    term_months: int
    disbursement_date: datetime
    maturity_date: datetime
    payment_frequency: str = "monthly"
    collateral_description: Optional[str] = None
    collateral_value: Optional[float] = None

class LoanCreate(LoanBase):
    customer_id: int

class LoanUpdate(BaseModel):
    current_balance: Optional[float] = None
    amount_due: Optional[float] = None
    next_payment_date: Optional[datetime] = None
    last_payment_date: Optional[datetime] = None
    loan_status: Optional[str] = None

class Loan(LoanBase):
    id: int
    customer_id: int
    current_balance: float
    outstanding_principal: float
    outstanding_interest: float
    amount_due: float
    loan_status: str
    created_at: datetime
    updated_at: datetime
    
    # Computed properties
    @property
    def monthly_payment(self) -> float:
        # Calculate EMI
        r = self.interest_rate / 100 / 12
        n = self.term_months
        p = self.principal_amount
        
        if r == 0:
            return p / n
        
        emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        return round(emi, 2)
    
    class Config:
        from_attributes = True