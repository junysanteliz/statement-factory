# backend/app/schemas/statement.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .customer import Customer
from .loan import Loan

class StatementRequest(BaseModel):
    customer_ids: List[int]
    loan_ids: List[int]
    period_start: datetime
    period_end: datetime
    format: str = "pdf"
    include_payment_history: bool = True
    include_charges_breakdown: bool = True

class StatementResponse(BaseModel):
    statement_id: str
    customer_id: int
    loan_id: int
    period_start: datetime
    period_end: datetime
    format: str
    download_url: Optional[str] = None
    generated_at: datetime

class BatchStatementRequest(BaseModel):
    statement_requests: List[StatementRequest]