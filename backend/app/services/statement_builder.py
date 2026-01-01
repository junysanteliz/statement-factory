from app.models.statement_models import StatementRequest

def build_statement_data(request: StatementRequest):
    """
    Prepares and enriches the statement data before it is passed
    to the PDF/Excel/TXT generators.
    """

    enriched_loans = []
    for loan in request.loans:
        monthly_interest = (loan.interest_rate / 100) / 12
        interest_amount = loan.current_balance * monthly_interest

        enriched_loans.append({
            "loan_id": loan.loan_id,
            "loan_type": loan.loan_type,
            "principal": loan.principal,
            "interest_rate": loan.interest_rate,
            "term_months": loan.term_months,
            "current_balance": loan.current_balance,
            "payment_due_date": loan.payment_due_date,
            "interest_amount": round(interest_amount, 2)
        })

    return {
        "customer": {
            "customer_id": request.customer.customer_id,
            "name": request.customer.name,
            "address": request.customer.address,
            "phone": request.customer.phone,
            "email": request.customer.email
        },
        "billing_period_start": request.billing_period_start,
        "billing_period_end": request.billing_period_end,
        "loans": enriched_loans
    }