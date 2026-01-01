from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import Optional


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
    customer = statement.customer
    loan = statement.loans[0] if statement.loans else None
    
    if not loan:
        raise ValueError("No loan data available for statement generation")
    
    # Sanitize customer data with defaults
    address = customer.address or "Address not provided"
    phone = customer.phone or "Phone not provided"
    email = customer.email or "Email not provided"
    
    # -------------------------------
    # 2. HEADER: Customer Info (Left)
    # -------------------------------
    c.setFont("Helvetica-Oblique", 20)
    c.drawString(margin, y, "Epimonos LLC")
    y -= 36  # Space after company name
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Loan Statement")
    
    c.setFont("Helvetica", 11)
    y -= 30  # Space after title
    
    # Draw customer info with tighter spacing to avoid overlap
    customer_lines = [
        customer.name,
        address,
        f"Phone: {phone}",
        f"Email: {email}"
    ]
    
    for line in customer_lines:
        c.drawString(margin, y, line)
        y -= 13  # Reduced from 15 for tighter spacing
    
    # Store the exact bottom of customer info
    customer_info_bottom = y + 13  # Add back one line height
    
    # -------------------------------
    # 3. HEADER: Metadata Table (Right) - FIXED WIDTH
    # -------------------------------
    meta_x = width - 200  # Reduced from 250 to prevent overflow
    meta_y = height - margin - 10
    
    # Metadata labels - with reduced font size
    c.setFont("Helvetica-Bold", 10)  # Reduced from 12
    c.drawRightString(meta_x - 5, meta_y, "Account Number:")
    c.drawRightString(meta_x - 5, meta_y - 15, "Billing Period:")
    c.drawRightString(meta_x - 5, meta_y - 30, "Statement Date:")
    
    # Metadata values - with wrapping/truncation for long text
    c.setFont("Helvetica", 10)  # Reduced from 12
    
    # Account number
    c.drawString(meta_x, meta_y, customer.customer_id[:15])  # Truncate if too long
    
    # Billing period - split if too long
    billing_period = f"{statement.billing_period_start} - {statement.billing_period_end}"
    if len(billing_period) > 25:
        # Split into two lines
        c.drawString(meta_x, meta_y - 15, billing_period[:25])
        c.drawString(meta_x, meta_y - 25, billing_period[25:50] + "...")
    else:
        c.drawString(meta_x, meta_y - 15, billing_period)
    
    # Statement date
    c.drawString(meta_x, meta_y - 30, datetime.now().strftime("%m/%d/%Y"))
    
    # -------------------------------
    # 4. GREEN HIGHLIGHT BOX (Payment Due) - POSITIONED SAFELY
    # -------------------------------
    # Position box with MORE space below customer info
    box_y = customer_info_bottom - 80  # Increased from 40 to 60 for more space
    box_height = 60  # Reduced from 60
    box_width = width - (2 * margin)
    
    # Draw green background
    c.setFillColorRGB(0.80, 0.95, 0.80)  # Light green
    c.roundRect(margin, box_y, box_width, box_height, 8, fill=1, stroke=0)  # Smaller radius
    
    # Draw text on green box
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)  # Reduced from 14
    c.drawString(margin + 15, box_y + 30,
                 f"Monthly Payment Due: ${loan.monthly_payment:,.2f}")
    
    c.setFont("Helvetica", 11)  # Reduced from 12
    c.drawString(margin + 15, box_y + 12,
                 f"Payment Due Date: {loan.payment_due_date}")
    
    # -------------------------------
    # 5. OVERVIEW SECTION
    # -------------------------------
    y = box_y - 35  # Space below green box
    
    c.setFont("Helvetica-Bold", 12)  # Reduced from 13
    c.drawString(margin, y, "Account Overview")
    
    # Overview items with aligned values
    y -= 20
    c.setFont("Helvetica", 10)  # Reduced from 11
    
    overview_items = [
        ("Previous Balance:", f"${loan.current_balance:,.2f}"),
        ("Interest Accrued:", "$0.00"),
        ("Fees:", "$0.00"),
        ("Current Balance:", f"${loan.current_balance:,.2f}")
    ]
    
    for label, value in overview_items:
        c.drawString(margin, y, label)
        c.drawString(margin + 180, y, value)  # Adjusted position
        y -= 14  # Reduced from 15
    
    # -------------------------------
    # 6. LOAN SUMMARY TABLE - FIXED COLUMN WIDTHS
    # -------------------------------
    y -= 25  # Additional space before table
    
    c.setFont("Helvetica-Bold", 13)  # Reduced from 13
    c.drawString(margin, y, "Loan Summary")
    
    y -= 18
    
    # Table headers with adjusted widths to fit page
    headers = ["Billing Period", "Monthly Payment", "Remaining Balance", "APR"]  # Changed "Remaining" to shorter label
    col_widths = [116, 106, 126, 66]  # Reduced widths
    
    c.setFont("Helvetica-Bold", 10)  # Reduced from 10
    x = margin
    for i, header in enumerate(headers):
        c.drawString(x, y, header)
        x += col_widths[i]
    
    # Table data row
    y -= 14
    c.setFont("Helvetica", 10)  # Reduced from 10
    x = margin
    
    # Truncate billing period if too long
    billing_period_cell = f"{statement.billing_period_start} - {statement.billing_period_end}"
    if len(billing_period_cell) > 18:
        billing_period_cell = billing_period_cell[:15] + "..."
    
    table_data = [
        billing_period_cell,
        f"${loan.monthly_payment:,.2f}",
        f"${loan.current_balance:,.2f}",
        f"{loan.interest_rate}%"
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
    # 7. FOOTER
    # -------------------------------
    footer_y = 40
    
    # Footer text
    c.setFont("Helvetica", 8)  # Reduced from 9
    c.setFillColor(colors.gray)
    c.drawString(margin, footer_y, 
                 "For questions or support, please reach out via email.")
    
    # Page number
    page_num = c.getPageNumber()
    c.drawRightString(width - margin, footer_y, f"Page {page_num}")
    
    # -------------------------------
    # 8. FINALIZE PDF
    # -------------------------------
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


# Alternative version with even more conservative spacing
def generate_pdf_conservative(statement) -> bytes:
    """More conservative version with guaranteed spacing."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    width, height = letter
    margin = 60  # Increased margin
    y = height - margin
    
    customer = statement.customer
    loan = statement.loans[0]
    
    # 1. TITLE
    c.setFont("Helvetica-Bold", 14)  # Smaller title
    c.drawString(margin, y, "LOAN STATEMENT")
    y -= 25
    
    # 2. CUSTOMER INFO (LEFT) - COMPACT
    c.setFont("Helvetica", 10)
    info_lines = [
        customer.name,
        customer.address or "",
        f"Ph: {customer.phone or 'N/A'}",
        f"Email: {customer.email or 'N/A'}"
    ]
    
    for line in info_lines:
        if line.strip():  # Only draw non-empty lines
            c.drawString(margin, y, line)
            y -= 12
    
    # 3. METADATA (RIGHT) - VERY COMPACT
    meta_y = height - margin - 10
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 150, meta_y, "Acct #:")
    c.drawRightString(width - 150, meta_y - 12, "Period:")
    c.drawRightString(width - 150, meta_y - 24, "Date:")
    
    c.setFont("Helvetica", 9)
    c.drawString(width - 145, meta_y, customer.customer_id[:10])
    
    # Truncate billing period aggressively
    period = f"{statement.billing_period_start} - {statement.billing_period_end}"
    if len(period) > 20:
        period = period[:17] + "..."
    c.drawString(width - 145, meta_y - 12, period)
    c.drawString(width - 145, meta_y - 24, datetime.now().strftime("%m/%d/%y"))
    
    # 4. GREEN BOX - WITH GUARANTEED CLEARANCE
    # Force box to start well below everything
    box_y = min(y, meta_y - 40) - 40  # Whichever is lower, minus buffer
    box_height = 45
    box_width = width - (2 * margin)
    
    c.setFillColorRGB(0.80, 0.95, 0.80)
    c.roundRect(margin, box_y, box_width, box_height, 5, fill=1, stroke=0)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 10, box_y + 25, f"Payment Due: ${loan.monthly_payment:,.2f}")
    
    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, box_y + 10, f"Due: {loan.payment_due_date}")
    
    # 5. CONTINUE WITH REST (using similar conservative sizing)
    y = box_y - 30
    
    # [Rest of the content with similarly reduced font sizes...]
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# Optional helper function for debugging layout
def _debug_draw_bounds(canvas_obj, x, y, width, height, color=(1, 0, 0)):
    """Draw a colored rectangle for debugging layout boundaries."""
    canvas_obj.setStrokeColorRGB(*color)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.rect(x, y, width, height)
    canvas_obj.setStrokeColor(colors.black)  # Reset to black