from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base
from typing import List, Optional

from .statement import Statement
from .customer import Customer

class Loan(Base):
    __tablename__ = "loans"
    
    # Correct: Use Mapped[] for type hints, mapped_column() for column definition
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_account_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    loan_type: Mapped[str] = mapped_column(String(50), nullable=False)
    principal_amount: Mapped[float] = mapped_column(Float, nullable=False)
    interest_rate: Mapped[float] = mapped_column(Float, nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    disbursement_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    maturity_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    current_balance: Mapped[float] = mapped_column(Float, default=0.0)
    amount_due: Mapped[float] = mapped_column(Float, default=0.0)
    next_payment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_payment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    loan_status: Mapped[str] = mapped_column(String(20), default="active")
    
     # Relationships using string references
    customer: Mapped["Customer"] = relationship("Customer", back_populates="loans")
    statements: Mapped[List["Statement"]] = relationship("Statement", back_populates="loan")
    
    # Property methods (these are safe - they run on instances, not columns)
    @property
    def is_overdue(self):
        """Check if loan payment is overdue"""
        if self.next_payment_date is None:  # ✅ Correct comparison
            return False
        return datetime.utcnow().date() > self.next_payment_date.date()
    
    @property
    def has_amount_due(self):
        """Check if there's an amount due"""
        return self.amount_due is not None and self.amount_due > 0  # ✅ Correct
    
    @property
    def monthly_payment(self):
        """Calculate monthly payment (EMI)"""
        if self.interest_rate == 0:  # ✅ Direct comparison works for simple values
            return self.principal_amount / self.term_months
        
        r: float = self.interest_rate / 100 / 12  # Monthly interest rate
        n: int = self.term_months                 # Total months
        p: float = self.principal_amount          # Principal
        
        emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        return round(emi, 2)
    
    def __repr__(self):
        return f"<Loan(id={self.id}, account={self.loan_account_number})>"