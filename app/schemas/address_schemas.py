from pydantic import BaseModel
from typing import Optional

# Base schema shared by all
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    is_primary: Optional[bool] = False  # Defaults to False if not provided
    phone_number: Optional[str] = None  # Now this field is optional
    vendor_id: Optional[int] = None  # Added support for multi-vendor addresses
    geolocation: Optional[str] = None  # Latitude and Longitude as a string (format: "lat,long")


# Create schema that inherits everything from AddressBase
class AddressCreate(AddressBase):
    pass  # No need to redefine fields from AddressBase


# Update schema should allow optional fields for partial updates
class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None
    phone_number: Optional[str] = None
    vendor_id: Optional[int] = None
    geolocation: Optional[str] = None


# Response schema that adds fields specific to the response
class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True  # This allows ORM models to be converted to Pydantic models
