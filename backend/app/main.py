from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import statements

app = FastAPI(
    title="Statement Generator API",
    version="1.0.0",
    description="Generates PDF, Excel, and Text loan statements."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(statements.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Statement Generator API is running"}