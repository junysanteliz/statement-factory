# app/services/utils.py
from typing import Tuple, Dict, Any
from datetime import datetime


def get_theme_color(loan_type: str) -> tuple:
    """
    Return RGB color tuple based on loan type for consistent theming.
    
    Args:
        loan_type: The type of loan (auto, rent, personal, mortgage, etc.)
        
    Returns:
        tuple: (R, G, B) values between 0-1
    """
    loan_type = loan_type.strip().lower() if loan_type else ""
    
    themes = {
        "rent": (0.75, 0.85, 0.95),      # Light blue
        "rental": (0.75, 0.85, 0.95),    # Light blue
        "lease": (0.75, 0.85, 0.95),     # Light blue
        "auto": (0.90, 0.85, 0.95),      # Light lavender
        "car": (0.90, 0.95, 0.85),       # Light green
        "vehicle": (0.90, 0.95, 0.85),   # Light green
        "personal": (0.95, 0.85, 0.90),  # Light pink
        "mortgage": (0.85, 0.90, 0.95),  # Light purple
        "home": (0.85, 0.90, 0.95),      # Light purple
        "house": (0.85, 0.90, 0.95),     # Light purple
        "student": (0.85, 0.95, 0.90),   # Mint green
        "education": (0.85, 0.95, 0.90), # Mint green
        "business": (0.95, 0.85, 0.90),  # Light pink
        "medical": (0.90, 0.85, 0.95),   # Light lavender
        "credit": (0.95, 0.95, 0.80),    # Light yellow
        "heloc": (0.80, 0.95, 0.95),     # Light cyan
    }
    
    return themes.get(loan_type, (0.80, 0.95, 0.80))  # Default green


def get_customers_from_statement(statement) -> list:
    """
    Safely extract customers from statement, handling both old and new formats.
    
    Args:
        statement: Statement object that may have 'customer' or 'customers' attribute
        
    Returns:
        list: List of customer objects
        
    Raises:
        ValueError: If no customer data found
    """
    if hasattr(statement, 'customers') and statement.customers:
        return statement.customers
    elif hasattr(statement, 'customer') and statement.customer:
        return [statement.customer]
    else:
        raise ValueError("No customer data found in statement")

def get_customer_terminology(loan_type: str, customer_count: int) -> dict:
    """Get appropriate terminology based on loan type and customer count."""
    loan_type = loan_type.lower() if loan_type else ""
    
    if loan_type in ["rent", "rental", "lease"]:
        return {
            "header_single": "Tenant:",
            "header_plural": "Tenants:",
            "address_label": "Property Address:",
            "individual_prefix": "Tenant"
        }
    elif loan_type in ["mortgage", "home", "house"]:
        return {
            "header_single": "Homeowner:",
            "header_plural": "Homeowners:",
            "address_label": "Property Address:",
            "individual_prefix": "Homeowner"
        }
    elif loan_type in ["auto", "car", "vehicle"]:
        return {
            "header_single": "Vehicle Owner:",
            "header_plural": "Vehicle Owners:",
            "address_label": "Address:",
            "individual_prefix": "Owner"
        }
    else:
        # Default loan terminology
        return {
            "header_single": "Borrower:",
            "header_plural": "Borrowers:",
            "address_label": "Address:",
            "individual_prefix": "Customer"
        }

def get_statement_type_config(loan_type: str) -> Dict[str, Any]:
    """
    Determine statement type and configuration based on loan type.
    
    Args:
        loan_type: The type of loan
        
    Returns:
        dict: Configuration dictionary with statement properties
    """
    loan_type = loan_type.strip().lower() if loan_type else ""
    
    is_rent = loan_type in ["rent", "rental", "lease"]
    
    # Mapping of loan types to display names
    type_display_map = {
        "auto": "Auto Loan",
        "car": "Auto Loan",
        "vehicle": "Auto Loan",
        "mortgage": "Mortgage",
        "home": "Mortgage",
        "house": "Mortgage",
        "personal": "Personal Loan",
        "rent": "Rent",
        "rental": "Rent",
        "lease": "Rent",
        "student": "Student Loan",
        "education": "Student Loan",
        "business": "Business Loan",
        "credit": "Credit Line",
        "heloc": "HELOC",
        "medical": "Medical Loan",
    }
    
    display_name = type_display_map.get(loan_type, loan_type.title() if loan_type else "Loan")
    
    return {
        "is_rent": is_rent,
        "display_name": display_name,
        "summary_title": "Activity Summary" if is_rent else "Loan Summary",
        "payment_label": "Monthly Rent" if is_rent else "Monthly Payment",
        "show_interest": not is_rent,
        "show_loan_type": not is_rent and loan_type not in ["", "loan"],
        "apr_label": "Rate" if is_rent else "APR",
        "default_apr": "N/A" if is_rent else f"0.00%",
    }


def get_statement_title(loan_type: str) -> str:
    """
    Get appropriate statement title based on loan type.
    
    Args:
        loan_type: The type of loan
        
    Returns:
        str: Formatted statement title
    """
    title_mapping = {
        "auto": "Auto Loan Statement",
        "car": "Auto Loan Statement",
        "vehicle": "Auto Loan Statement",
        "mortgage": "Mortgage Statement",
        "home": "Mortgage Statement",
        "house": "Mortgage Statement",
        "personal": "Personal Loan Statement",
        "rent": "Rent Statement",
        "rental": "Rent Statement",
        "lease": "Rent Statement",
        "student": "Student Loan Statement",
        "education": "Student Loan Statement",
        "business": "Business Loan Statement",
        "credit": "Credit Line Statement",
        "heloc": "HELOC Statement",
        "medical": "Medical Loan Statement",
    }
    
    if loan_type in title_mapping:
        return title_mapping[loan_type]
    elif loan_type:
        return f"{loan_type.title()} Loan Statement"
    else:
        return "Loan Statement"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with optional suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        suffix: Suffix to add when truncated
        
    Returns:
        str: Truncated text if necessary
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_currency(amount: float) -> str:
    """
    Format currency amount with commas and 2 decimal places.
    
    Args:
        amount: Currency amount
        
    Returns:
        str: Formatted currency string
    """
    try:
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"


def get_current_date(format_str: str = "%m/%d/%Y") -> str:
    """
    Get current date formatted as string.
    
    Args:
        format_str: Date format string
        
    Returns:
        str: Formatted current date
    """
    return datetime.now().strftime(format_str)


def debug_draw_bounds(canvas_obj, x: float, y: float, width: float, height: float, color: Tuple[float, float, float] = (1, 0, 0)):
    """
    Draw a colored rectangle for debugging layout boundaries.
    
    Args:
        canvas_obj: ReportLab canvas object
        x: X coordinate
        y: Y coordinate
        width: Rectangle width
        height: Rectangle height
        color: RGB color tuple
    """
    canvas_obj.setStrokeColorRGB(*color)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.rect(x, y, width, height)
    # Reset to black - import colors in calling function