from pydantic import BaseModel, field_validator
from .customer import Customer
from typing import List, Optional

class Loan(BaseModel):
    loan_id: str
    loan_type: str
    principal: float
    interest_rate: float
    term_months: int
    current_balance: float
    payment_due_date: str
    monthly_payment: float  # NEW

# OPTION 1: Support both single and multiple customers
class StatementRequest(BaseModel):
    # Keep customer for backward compatibility
    customer: Optional[Customer] = None
    # Add customers for new frontend
    customers: Optional[List[Customer]] = None
    loans: List[Loan]
    billing_period_start: str
    billing_period_end: str
    statement_format: str

    # Validator to ensure at least one customer is provided
    @field_validator('customers', mode='before')
    @classmethod
    def validate_customers(cls, v, values):
        # If neither customer nor customers is provided, raise error
        if v is None and values.get('customer') is None:
            raise ValueError('Either customer or customers must be provided')
        return v

# OPTION 2: Only support multiple customers (cleaner)
class MultiCustomerStatementRequest(BaseModel):
    customers: List[Customer]
    loans: List[Loan]
    billing_period_start: str
    billing_period_end: str
    statement_format: str
