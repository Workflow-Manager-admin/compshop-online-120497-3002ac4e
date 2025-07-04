from fastapi import FastAPI, status, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List

app = FastAPI(
    title="Computer Shop Backend API",
    description="Backend for computer shop website. Provides product listing, shop info, and manages user inquiries.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Products", "description": "Product listing endpoints"},
        {"name": "Shop", "description": "Shop information endpoints"},
        {"name": "Inquiries", "description": "Contact/inquiry endpoints"}
    ]
)

# Allow all origins for the frontend (adjust in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Data models
# -------------------------

class Product(BaseModel):
    """Represents a computer shop product."""
    id: int = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Price of the product")
    in_stock: bool = Field(..., description="Availability in shop")

class ShopInfo(BaseModel):
    """Represents general information about the shop."""
    name: str = Field(..., description="Computer shop name")
    address: str = Field(..., description="Physical address")
    phone: str = Field(..., description="Contact phone number")
    email: EmailStr = Field(..., description="Shop contact email")
    description: str = Field(..., description="Short description about the shop")

class Inquiry(BaseModel):
    """Represents a contact form submission from a user."""
    name: str = Field(..., description="Name of the user")
    email: EmailStr = Field(..., description="User's contact email")
    message: str = Field(..., description="Inquiry or message content")

class InquiryResponse(BaseModel):
    """Server response for a submitted inquiry."""
    detail: str = Field(..., description="Server message")

# ------------------------------------------------------
# Example in-memory data (replace with DB in production)
# ------------------------------------------------------

_fake_products = [
    Product(id=1, name="Gaming Laptop", description="High-end RTX 4070Ti, 32GB RAM", price=1999.99, in_stock=True),
    Product(id=2, name="Mechanical Keyboard", description="RGB, Cherry MX Blue switches", price=119.99, in_stock=True),
    Product(id=3, name="24\" Monitor", description="1080p, 144Hz, IPS", price=179.99, in_stock=False),
]
_fake_shop_info = ShopInfo(
    name="BytePC Computers",
    address="123 Tech Street, Silicon City",
    phone="555-123-4567",
    email="info@bytepc.com",
    description="Your local experts in computers and accessories. Established 2020."
)

# -------------------------
# API Endpoints
# -------------------------

# PUBLIC_INTERFACE
@app.get("/", tags=["Shop"])
def health_check():
    """Health check endpoint for the backend."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/products", response_model=List[Product], tags=["Products"], summary="Get product list", description="Returns the list of computer shop products.")
def get_products():
    """
    Returns all available products.

    Returns:
        List of Product details.
    """
    # BUSINESS LOGIC: Replace with DB call in the future
    return _fake_products

# PUBLIC_INTERFACE
@app.get("/shop-info", response_model=ShopInfo, tags=["Shop"], summary="Get shop information", description="Returns information about the computer shop.")
def get_shop_info():
    """
    Provides general information about the shop.

    Returns:
        ShopInfo object.
    """
    # BUSINESS LOGIC: Replace with DB call in the future
    return _fake_shop_info

# PUBLIC_INTERFACE
@app.post("/inquiry", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED, tags=["Inquiries"], summary="Submit contact inquiry", description="Submit a contact or inquiry message to the shop.")
def submit_inquiry(inquiry: Inquiry = Body(..., description="Inquiry data")):
    """
    Receives and processes a user inquiry.

    Args:
        inquiry: User-submitted inquiry information.

    Returns:
        InquiryResponse with confirmation message.
    """
    # BUSINESS LOGIC: Save inquiry to DB, send email/notification, etc.
    # Currently just simulates storing the inquiry
    print(f"Received inquiry: {inquiry}")  # Simulate action
    return InquiryResponse(detail="Your inquiry has been received. We'll get back to you soon.")

