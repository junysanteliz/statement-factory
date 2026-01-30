# backend/app/models/transaction.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class TransactionType(enum.Enum):
    PAYMENT = "payment"
    INTEREST = "interest"
    FEE = "fee"
    ADJUSTMENT = "adjustment"
    DISBURSEMENT = "disbursement"

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), unique=True, index=True, nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    posting_date = Column(DateTime)
    transaction_type = Column(String(20), nullable=False)  # Using String for flexibility
    amount = Column(Float, nullable=False)
    principal_amount = Column(Float, default=0.0)
    interest_amount = Column(Float, default=0.0)
    fees_amount = Column(Float, default=0.0)
    description = Column(String(255))
    reference_number = Column(String(100))
    status = Column(String(20), default="completed")
    payment_method = Column(String(50))  # cash, check, transfer, card
    check_number = Column(String(50))
    created_by = Column(String(100))  # User/system that created the transaction
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    loan = relationship("Loan", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"