def generate_text(statement):
    lines = [
        "LOAN STATEMENT",
        "",
        f"Customer: {statement.customer_name}",
        f"Customer ID: {statement.customer_id}",
        f"Billing Period: {statement.billing_period_start} - {statement.billing_period_end}",
        ""
    ]

    for loan in statement.loans:
        lines += [
            f"Loan Type: {loan.loan_type}",
            f"  Principal: {loan.principal}",
            f"  Interest Rate: {loan.interest_rate}%",
            f"  Current Balance: {loan.current_balance}",
            f"  Payment Due: {loan.payment_due_date}",
            ""
        ]

    return "\n".join(lines)