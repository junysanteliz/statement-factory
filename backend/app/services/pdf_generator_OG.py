from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(statement):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont("Helvetica-Bold", 24)
    c.drawString(200, 800, "Loan Statement")

    c.setFont("Helvetica", 14)
    c.drawString(50, 770, f"Customer: {statement.customer_name}")
    c.drawString(50, 755, f"Customer ID: {statement.customer_id}")
    c.drawString(50, 740, f"Billing Period: {statement.billing_period_start} - {statement.billing_period_end}")

    y = 700
    for loan in statement.loans:
        c.drawString(50, y, f"Loan Type: {loan.loan_type}")
        c.drawString(50, y - 15, f"Principal: {loan.principal}")
        c.drawString(50, y - 30, f"Interest Rate: {loan.interest_rate}%")
        c.drawString(50, y - 45, f"Current Balance: {loan.current_balance}")
        c.drawString(50, y - 60, f"Payment Due Date: {loan.payment_due_date}")
        y -= 90

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf