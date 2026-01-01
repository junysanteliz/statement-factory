from fastapi import APIRouter, Response
from app.models.statement_models import StatementRequest
from app.services.pdf_generator import generate_pdf
from app.services.excel_generator import generate_excel
from app.services.text_generator import generate_text

router = APIRouter()

@router.post("/statements", response_class=Response)
async def create_statement(request: StatementRequest):

    customer_id = request.customer.customer_id

    if request.statement_format == "pdf":
        pdf_bytes = generate_pdf(request)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=statement_{customer_id}.pdf"
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