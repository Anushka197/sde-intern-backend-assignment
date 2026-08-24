from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import init_db
from app.routes.customers import router as customers_router
from app.routes.items import router as items_router
# from app.routes.invoices import router as invoices_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Teardown logic (if needed)


app = FastAPI(
    title="REST API Boilerplate",
    description="FastAPI + SQLModel Boilerplate",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(customers_router)
app.include_router(items_router)
# app.include_router(invoices_router)

# Redirect error code 422 to 400 for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )
    
@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
def health_check():
    return JSONResponse(content={"status": "healthy", "service": "running"})