from fastapi import APIRouter, Response, HTTPException
from app.models.statement_models import StatementRequest
from app.services.pdf_generator import generate_pdf
from app.services.excel_generator import generate_excel
from app.services.text_generator import generate_text

router = APIRouter()

### NEW ROUTE FOR MULTI-CUSTOMER STATEMENTS i.e. 2 or more customers per statement ###
@router.post("/generate-statement", response_class=Response)
async def create_multi_cust_statement(request: StatementRequest):

    # Multiple customers - use first customer for ID
    if not request.customers:
        raise HTTPException(status_code=400, detail="No customers provided")
    
    primary_customer = request.customers[0]
    customer_id = primary_customer.customer_id

    if request.statement_format == "pdf":
        pdf_bytes = generate_pdf(request)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=joint_statement_{customer_id}.pdf"
            }
        )

    if request.statement_format == "xlsx":
        excel_bytes = generate_excel(request)
        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=statement_{customer_id}.xlsx"
            }
        )

    if request.statement_format == "txt":
        text_data = generate_text(request)
        return Response(
            content=text_data,
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename=statement_{customer_id}.txt"
            }
        )