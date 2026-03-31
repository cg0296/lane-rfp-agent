from fastapi import FastAPI, HTTPException, staticfiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

from app.config import settings
from app.models import (
    EmailParseRequest,
    EmailParseResponse,
    ParsedQuoteData,
    QuoteGenerationRequest,
    QuoteGenerationResponse,
    Carrier,
    CarrierCreate,
)
from app.agents.email_parser import parse_email
from app.excel_generator import generate_quote_sheet

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve downloads directory
os.makedirs("downloads", exist_ok=True)
app.mount("/downloads", staticfiles.StaticFiles(directory="downloads"), name="downloads")

# In-memory carrier storage (will move to database)
carriers_db: dict[int, Carrier] = {}
next_carrier_id = 1


# Default carriers for MVP
DEFAULT_CARRIERS = [
    {"id": 1, "name": "Carrier A", "email": "quotes@carriera.com", "phone": "123-456-7890"},
    {"id": 2, "name": "Carrier B", "email": "rates@carrierb.com", "phone": "234-567-8901"},
    {"id": 3, "name": "Carrier C", "email": "dispatch@carrierc.com", "phone": "345-678-9012"},
]

for carrier in DEFAULT_CARRIERS:
    carriers_db[carrier["id"]] = Carrier(**carrier)

next_carrier_id = max(carriers_db.keys(), default=0) + 1


# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}


# Email parsing endpoint
@app.post("/api/parse-email", response_model=EmailParseResponse)
async def parse_email_endpoint(request: EmailParseRequest):
    """
    Parse a client email to extract quote details.

    Returns structured data ready for quote sheet generation.
    """
    try:
        parsed_data = parse_email(request.email_text, request.client_name)
        return EmailParseResponse(success=True, data=parsed_data)
    except ValueError as e:
        return EmailParseResponse(success=False, error=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing email: {str(e)}")


# Quote generation endpoint
@app.post("/api/generate-quote-sheet", response_model=QuoteGenerationResponse)
async def generate_quote_sheet_endpoint(request: QuoteGenerationRequest):
    """
    Generate an Excel quote sheet from parsed data and carriers.
    """
    try:
        file_path, filename = generate_quote_sheet(
            quote_data=request.quote_data,
            carriers=request.carriers,
            client_name=request.client_name or "Quote"
        )

        # Return download URL
        return QuoteGenerationResponse(
            success=True,
            file_url=f"/downloads/{filename}",
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quote sheet: {str(e)}")


# Download quote sheet
@app.get("/api/downloads/{filename}")
async def download_quote(filename: str):
    """Download a generated quote sheet."""
    file_path = os.path.join("downloads", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )


# Carrier management endpoints
@app.get("/api/carriers", response_model=List[Carrier])
async def get_carriers():
    """Get all carriers."""
    return list(carriers_db.values())


@app.post("/api/carriers", response_model=Carrier)
async def create_carrier(carrier: CarrierCreate):
    """Add a new carrier."""
    global next_carrier_id
    new_id = next_carrier_id
    next_carrier_id += 1

    new_carrier = Carrier(
        id=new_id,
        name=carrier.name,
        email=carrier.email,
        phone=carrier.phone
    )

    carriers_db[new_id] = new_carrier
    return new_carrier


@app.delete("/api/carriers/{carrier_id}")
async def delete_carrier(carrier_id: int):
    """Delete a carrier."""
    if carrier_id not in carriers_db:
        raise HTTPException(status_code=404, detail="Carrier not found")

    del carriers_db[carrier_id]
    return {"status": "deleted"}


# Root endpoint
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )
