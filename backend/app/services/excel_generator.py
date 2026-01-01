from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font
from io import BytesIO

def generate_excel(statement):
    wb = Workbook()
    ws: Worksheet = wb.active  # type: ignore # tell Pylance this is a Worksheet
    ws.title = "Statement"


    ws.append(["Loan Statement"])
    ws.append([])
    ws.append(["Customer Name", statement.customer_name])
    ws.append(["Customer ID", statement.customer_id])
    ws.append(["Billing Period", f"{statement.billing_period_start} - {statement.billing_period_end}"])
    ws.append([])

    ws.append(["Loan Type", "Principal", "Interest Rate", "Current Balance", "Payment Due Date"])

    for loan in statement.loans:
        ws.append([
            loan.loan_type,
            loan.principal,
            loan.interest_rate,
            loan.current_balance,
            loan.payment_due_date
        ])

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()