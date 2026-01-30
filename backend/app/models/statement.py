# backend/app/models/statement.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Statement(Base):
    __tablename__ = "statements"
    
    id = Column(Integer, primary_key=True, index=True)
    statement_id = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(100))  # User/system that generated the statement
    format = Column(String(10), default="pdf")  # pdf, excel, txt
    file_path = Column(String(500))  # Path to stored file
    file_size = Column(Integer)  # Size in bytes
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    sent_via = Column(String(50))  # email, mail, download
    opening_balance = Column(Float, default=0.0)
    closing_balance = Column(Float, default=0.0)
    total_principal_paid = Column(Float, default=0.0)
    total_interest_paid = Column(Float, default=0.0)
    total_fees_paid = Column(Float, default=0.0)
    total_payments = Column(Float, default=0.0)
    next_payment_due = Column(Float, default=0.0)
    next_payment_date = Column(DateTime)
    is_final = Column(Boolean, default=False)  # Final statement for closed loans
    statement_metadata = Column(Text)  # JSON metadata about generation
    
    # Relationships
    customer = relationship("Customer", back_populates="statements")
    loan = relationship("Loan", back_populates="statements")
    
    def __repr__(self):
        return f"<Statement(id={self.id}, statement_id={self.statement_id}, period={self.period_start.date()}-{self.period_end.date()})>"