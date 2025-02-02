from pydantic import BaseModel
from typing import Optional

# Base schema shared by all
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postalCode: str
    country: str
    is_primary: Optional[bool] = False  # Defaults to False if not provided
    phoneNumber: Optional[str] = None  # Now this field is optional
    sellerId: Optional[str] = None  # Added support for multi-vendor addresses
    geolocation: Optional[str] = None  # Latitude and Longitude as a string (format: "lat,long")


# Create schema that inherits everything from AddressBase
class AddressCreate(AddressBase):
    pass  # No need to redefine fields from AddressBase


# Update schema should allow optional fields for partial updates
class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None
    phoneNumber: Optional[str] = None
    sellerId: Optional[str] = None
    geolocation: Optional[str] = None


# Response schema that adds fields specific to the response
class AddressResponse(AddressBase):
    id: int
    user_id: str

    class Config:
        orm_mode = True  # This allows ORM models to be converted to Pydantic models
