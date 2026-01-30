# backend/app/routers/statements.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.schemas.statement import StatementRequest, StatementResponse, BatchStatementRequest
from app.crud import customer_crud, loan_crud
from app.services.statement_service import StatementService
from app.generators.pdf_generator import PDFStatementGenerator
from app.generators.excel_generator import ExcelStatementGenerator
from app.models.statement import Statement as StatementModel

router = APIRouter()

@router.post("/generate", response_model=StatementResponse)
async def generate_statement(
    request: StatementRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a single loan statement using database data
    """
    try:
        # Validate customers exist
        customers = []
        for customer_id in request.customer_ids:
            customer = customer_crud.get_customer(db, customer_id)
            if not customer:
                raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")
            customers.append(customer)
        
        # Validate loans exist and belong to customers
        loans = []
        for loan_id in request.loan_ids:
            loan = loan_crud.get_loan(db, loan_id)
            if not loan:
                raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
            
            # Check if loan belongs to any of the requested customers
            if loan.customer_id not in request.customer_ids:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Loan {loan_id} does not belong to any of the specified customers"
                )
            loans.append(loan)
        
        # Prepare statement data
        statement_data = await _prepare_statement_data_from_db(db, customers, loans, request)
        
        # Generate statement
        if request.format == "pdf":
            generator = PDFStatementGenerator()
            content = generator.generate_statement(statement_data)
            media_type = "application/pdf"
            filename = f"statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        elif request.format == "excel":
            generator = ExcelStatementGenerator()
            content = generator.generate_statement(statement_data)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = f"statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        elif request.format == "txt":
            from app.generators.text_generator import TextStatementGenerator
            generator = TextStatementGenerator()
            content = generator.generate_statement(statement_data)
            media_type = "text/plain"
            filename = f"statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        # Create statement record in database
        statement_id = f"STMT{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
        
        db_statement = StatementModel(
            statement_id=statement_id,
            customer_id=customers[0].id,  # Primary customer
            loan_id=loans[0].id if loans else None,
            period_start=request.period_start,
            period_end=request.period_end,
            format=request.format,
            generated_by="system",
            opening_balance=statement_data.get('opening_balance', 0),
            closing_balance=statement_data.get('closing_balance', 0)
        )
        
        db.add(db_statement)
        db.commit()
        
        # Return response with download info
        return StatementResponse(
            statement_id=statement_id,
            customer_id=customers[0].id,
            loan_id=loans[0].id if loans else None,
            period_start=request.period_start,
            period_end=request.period_end,
            format=request.format,
            download_url=f"/api/v1/statements/download/{statement_id}",
            generated_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def _prepare_statement_data_from_db(db, customers, loans, request):
    """
    Prepare statement data from database records
    """
    # This would fetch actual transaction data, charges, etc.
    # Simplified example:
    
    primary_customer = customers[0]
    primary_loan = loans[0] if loans else None
    
    # Fetch transactions for the period
    # In production, you'd query the Transaction model
    from datetime import datetime, timedelta
    import random
    
    # Mock transactions for example
    transactions = []
    if request.include_payment_history and primary_loan:
        # Generate mock transaction data
        current_date = request.period_start
        balance = primary_loan.current_balance
        
        while current_date <= request.period_end:
            if random.random() > 0.7:  # 30% chance of a payment each "period"
                amount = primary_loan.monthly_payment
                principal = amount * 0.7
                interest = amount * 0.3
                balance -= principal
                
                transactions.append({
                    "date": current_date,
                    "description": "Monthly Payment",
                    "amount": amount,
                    "principal": principal,
                    "interest": interest,
                    "balance": max(balance, 0)
                })
            
            current_date += timedelta(days=30)
    
    # Prepare response data
    return {
        "statement_period": {
            "start": request.period_start,
            "end": request.period_end
        },
        "customers": [{
            "id": c.id,
            "customer_id": c.customer_id,
            "name": c.full_name,
            "email": c.email,
            "address": f"{c.address}, {c.city}, {c.state} {c.postal_code}",
            "phone": c.phone
        } for c in customers],
        "loans": [{
            "account_number": l.loan_account_number,
            "type": l.loan_type,
            "principal": l.principal_amount,
            "interest_rate": l.interest_rate,
            "current_balance": l.current_balance,
            "outstanding_principal": l.outstanding_principal,
            "monthly_payment": l.monthly_payment,
            "next_payment_date": l.next_payment_date,
            "amount_due": l.amount_due
        } for l in loans],
        "transactions": transactions,
        "include_payment_history": request.include_payment_history,
        "include_charges_breakdown": request.include_charges_breakdown
    }