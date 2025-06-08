# app/main.py
import uvicorn
from fastapi import FastAPI

from app.api.endpoints import maintenance, products, suppliers
from app.core.config import settings

app = FastAPI(title="Smart Inventory & Order Management System")

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Inventory API"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        log_level="info",
    )
