from pydantic import BaseModel
from .customer import Customer
from typing import List

class Loan(BaseModel):
    loan_id: str
    loan_type: str
    principal: float
    interest_rate: float
    term_months: int
    current_balance: float
    payment_due_date: str
    monthly_payment: float  # NEW

class StatementRequest(BaseModel):
    customer: Customer
    billing_period_start: str
    billing_period_end: str
    loans: List[Loan]
    statement_format: str  # "pdf" | "xlsx" | "txt"
