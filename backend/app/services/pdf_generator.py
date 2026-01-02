# app/services/pdf_generator.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from typing import Optional
from .utils import (
    format_payment_due_date,
    get_customer_terminology,
    get_theme_color,
    get_customers_from_statement,
    get_statement_type_config,
    get_statement_title,
    truncate_text,
    format_currency,
    get_current_date
)


def generate_pdf(statement) -> bytes:
    """
    Generate a PDF loan statement with proper layout and spacing.
    
    Args:
        statement: Object containing customer, loan, and billing information
        
    Returns:
        bytes: PDF file content as bytes
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Page settings
    width, height = letter
    margin = 50
    y = height - margin
    
# -------------------------------
# 1. DATA VALIDATION & SANITIZATION
# -------------------------------
    customers = get_customers_from_statement(statement)

    if not statement.loans:
        raise ValueError("No loan data available for statement generation")

    loan = statement.loans[0]
    loan_type = loan.loan_type.strip().lower() if hasattr(loan, 'loan_type') and loan.loan_type else ""
    statement_config = get_statement_type_config(loan_type)
    is_rent_statement = statement_config["is_rent"]

    # Get primary customer for legacy fields (e.g., for account number fallback)
    primary_customer = customers[0]
# -------------------------------
# 2. DYNAMIC TITLE & COMPANY HEADER
# -------------------------------
    c.setFont("Helvetica-Oblique", 20)
    c.drawString(margin, y, "Epimonos LLC")
    y -= 36

# Determine statement title
    statement_title = get_statement_title(loan_type)
    if len(customers) > 1:
        statement_title = "Joint Tenancy Statement" if is_rent_statement else "Joint Account Statement"

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, statement_title)
    y -= 30

# -------------------------------
# 3. CUSTOMER INFO SECTION - OPTIMIZED FOR JOINT TENANTS
# -------------------------------
    c.setFont("Helvetica-Bold", 11)

# Then use it in your PDF generator:
    terminology = get_customer_terminology(loan_type, len(customers))

# Draw header
    header_text = terminology["header_plural"] if len(customers) > 1 else terminology["header_single"]
    c.drawString(margin, y, header_text)
    y -= 20

# Draw names
    customer_names = ", ".join([cust.name for cust in customers])
    c.drawString(margin, y, customer_names)
    y -= 20

# Draw address with label
    if primary_customer.address:
        c.drawString(margin, y, f"{terminology['address_label']} {primary_customer.address}")
        y -= 20

# Display INDIVIDUAL contact details in a compact format
    for i, customer in enumerate(customers):
        contact_info = []
        if customer.phone:
            contact_info.append(f"Ph: {customer.phone}")
        if customer.email:
            contact_info.append(f"Email: {customer.email}")
    
        if contact_info:
            # For multiple customers, you might want to label them
            if len(customers) > 1:
                c.drawString(margin, y, f"Contact {i+1}: {', '.join(contact_info)}")
            else:
                c.drawString(margin, y, f"Contact: {', '.join(contact_info)}")
            y -= 18

# Store the bottom of customer info
    customer_info_bottom = y + 5  # Small buffer
    
    # -------------------------------
    # 4. METADATA TABLE (Right)
    # -------------------------------
    meta_x = width - 200
    meta_y = height - margin - 10
    
    # Metadata labels
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(meta_x - 5, meta_y, "Account Number:")
    c.drawRightString(meta_x - 5, meta_y - 15, "Billing Period:")
    c.drawRightString(meta_x - 5, meta_y - 30, "Statement Date:")
    
    # Metadata values
    c.setFont("Helvetica", 10)
    
    # Account number
    account_number = loan.loan_id if hasattr(loan, 'loan_id') and loan.loan_id else customer.customer_id
    c.drawString(meta_x, meta_y, truncate_text(str(account_number), 15))
    
    # Billing period
    billing_period = f"{statement.billing_period_start} - {statement.billing_period_end}"
    if len(billing_period) > 25:
        c.drawString(meta_x, meta_y - 15, truncate_text(billing_period, 25, ""))
        c.drawString(meta_x, meta_y - 25, truncate_text(billing_period[25:], 25))
    else:
        c.drawString(meta_x, meta_y - 15, billing_period)
    
    # Statement date
    c.drawString(meta_x, meta_y - 30, get_current_date())
    
    # -------------------------------
    # 5. HIGHLIGHT BOX (Payment Due)
    # -------------------------------
    box_y = customer_info_bottom - 80
    box_height = 80
    box_width = width - (2 * margin)
    
    # Get theme color based on loan type
    theme_color = get_theme_color(loan_type)
    c.setFillColorRGB(*theme_color)
    c.roundRect(margin, box_y, box_width, box_height, 8, fill=1, stroke=0)
    
    # Draw text on colored box
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    
    # Use appropriate payment text based on statement type
    if loan_type == "rent to own":
    # Special case for "Rent to own"
        payment_title = f"Monthly Rent To Own Payment Due: {format_currency(float(loan.monthly_payment))}"
    elif is_rent_statement:
    # Regular rent/lease/rental
        payment_title = f"Monthly Rent Due: {format_currency(float(loan.monthly_payment))}"
    else:
    # All other loan types (auto, personal, mortgage, etc.)
        payment_prefix = f"{loan_type.title()} " if loan_type and loan_type != "loan" else ""
        payment_title = f"Monthly {payment_prefix}Payment Due: {format_currency(float(loan.monthly_payment))}"
    
    c.drawString(margin + 15, box_y + 50, payment_title.strip())
    
    c.setFont("Helvetica-Bold", 11)
    # ✅ FORMAT THE PAYMENT DUE DATE
    formatted_due_date = format_payment_due_date(loan.payment_due_date)
    c.drawString(margin + 15, box_y + 32, f"Payment Due Date: {formatted_due_date}")
    c.setFont("Helvetica", 11)
    c.drawString(margin + 15, box_y + 16, f"*Please make your payment within the 10 day grace period as stated in the contract.")
    
    # -------------------------------
    # 6. OVERVIEW SECTION
    # -------------------------------
    y = box_y - 35
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Account Overview")
    
    y -= 20
    c.setFont("Helvetica", 10)
    
    # Build overview items conditionally
    overview_items = [
        ("Previous Balance:", format_currency(float(loan.current_balance))),
    ]
    
    # Only include "Interest Accrued" for non-rent statements
    if not is_rent_statement:
        overview_items.append(("Interest Accrued:", "$0.00"))
    
    overview_items.extend([
        ("Fees:", "$0.00"),
        ("Current Balance:", format_currency(float(loan.current_balance)))
    ])
    
    for label, value in overview_items:
        c.drawString(margin, y, label)
        c.drawString(margin + 180, y, value)
        y -= 14
    
    # -------------------------------
    # 7. LOAN/RENT SUMMARY TABLE
    # -------------------------------
    y -= 25
    
    # Use appropriate summary title
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, statement_config["summary_title"])
    
    y -= 18
    
    # Table headers
    headers = ["Billing Period", "Monthly Payment", "Remaining Balance", "APR"]
    col_widths = [136, 106, 126, 66]
    
    # For rent statements, adjust the header text
    if is_rent_statement:
        headers = ["Billing Period", "Monthly Rent", "Remaining Balance", "Rate"]
    
    c.setFont("Helvetica-Bold", 10)
    x = margin
    for i, header in enumerate(headers):
        c.drawString(x, y, header)
        x += col_widths[i]
    
    # Table data row
    y -= 14
    c.setFont("Helvetica", 10)
    x = margin
    
    billing_period_cell = f"{statement.billing_period_start} - {statement.billing_period_end}"
    billing_period_cell = truncate_text(billing_period_cell, 25)
    
    # For rent statements, show N/A for APR
    apr_value = f"{loan.interest_rate}%" if not is_rent_statement else "N/A"
    
    table_data = [
        billing_period_cell,
        format_currency(float(loan.monthly_payment)),
        format_currency(float(loan.current_balance)),
        apr_value
    ]
    
    for i, cell in enumerate(table_data):
        c.drawString(x, y, cell)
        x += col_widths[i]
    
    # Draw table border
    y -= 5
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.5)
    c.line(margin, y, width - margin, y)
    
    # -------------------------------
    # 8. ADD LOAN TYPE IN SUMMARY (Only for non-rent statements)
    # -------------------------------
    if not is_rent_statement and hasattr(loan, 'loan_type') and loan.loan_type:
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, f"Loan Type: {loan.loan_type}")
    
    # -------------------------------
    # 9. FOOTER
    # -------------------------------
    footer_y = 40
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.gray)
    
    # Customize footer message based on statement type
    if is_rent_statement:
        c.drawString(margin, footer_y, "For questions about your rent or lease, please contact your property manager.")
    else:
        c.drawString(margin, footer_y, "For questions or support, please reach out via email.")
    
    # Page number
    page_num = c.getPageNumber()
    c.drawRightString(width - margin, footer_y, f"Page {page_num}")
    
    # -------------------------------
    # 10. FINALIZE PDF
    # -------------------------------
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


def generate_pdf_conservative(statement) -> bytes:
    """
    More conservative version with guaranteed spacing and smaller fonts.
    Useful for statements with lots of content.
    """
    from .utils import get_current_date
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    width, height = letter
    margin = 60  # Increased margin
    y = height - margin
    
    customers = get_customers_from_statement(statement)
    customer = customers[0]
    loan = statement.loans[0]
    
    # 1. TITLE
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "LOAN STATEMENT")
    y -= 25
    
    # 2. CUSTOMER INFO - COMPACT
    c.setFont("Helvetica", 10)
    info_lines = [
        customer.name,
        customer.address or "",
        f"Ph: {customer.phone or 'N/A'}",
        f"Email: {customer.email or 'N/A'}"
    ]
    
    for line in info_lines:
        if line.strip():
            c.drawString(margin, y, line)
            y -= 12
    
    # 3. METADATA - VERY COMPACT
    meta_y = height - margin - 10
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 150, meta_y, "Acct #:")
    c.drawRightString(width - 150, meta_y - 12, "Period:")
    c.drawRightString(width - 150, meta_y - 24, "Date:")
    
    c.setFont("Helvetica", 9)
    c.drawString(width - 145, meta_y, customer.customer_id[:10])
    
    # Billing period
    period = f"{statement.billing_period_start} - {statement.billing_period_end}"
    period = truncate_text(period, 20)
    c.drawString(width - 145, meta_y - 12, period)
    c.drawString(width - 145, meta_y - 24, get_current_date("%m/%d/%y"))
    
    # 4. HIGHLIGHT BOX
    box_y = min(y, meta_y - 40) - 40
    box_height = 45
    box_width = width - (2 * margin)
    
    # Get theme color
    loan_type = loan.loan_type.lower() if hasattr(loan, 'loan_type') and loan.loan_type else ""
    theme_color = get_theme_color(loan_type)
    c.setFillColorRGB(*theme_color)
    c.roundRect(margin, box_y, box_width, box_height, 5, fill=1, stroke=0)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 10, box_y + 25, f"Payment Due: {format_currency(float(loan.monthly_payment))}")
    
    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, box_y + 10, f"Due: {loan.payment_due_date}")
    
    # Continue with rest of content...
    # You would add the rest of your conservative layout here
    
    c.save()
    return buffer.getvalue()