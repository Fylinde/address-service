from sqlalchemy.orm import Session
from app.models.address import AddressModel
from app.schemas.address_schemas import AddressCreate, AddressUpdate
from fastapi import HTTPException
import requests
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# You can configure the base URL of the user-service here
USER_SERVICE_URL = "http://user-service/users"

def validate_user(user_id: int):
    """
    Validate user by making an API call to user-service.
    """
    try:
        response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        logger.error(f"Error validating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate user")

def create_address(db: Session, address_data: AddressCreate, user_id: int, vendor_id: int = None):
    """
    Create a new address for a user.
    Decoupled: Validates user through API, supports vendor-specific addresses.
    """
    try:
        # Validate user via user-service API
        validate_user(user_id)
        
        # Create a new address
        new_address = AddressModel(
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            postal_code=address_data.postal_code,
            country=address_data.country,
            phone_number=address_data.phone_number,
            user_id=user_id,
            vendor_id=vendor_id,  # Multivendor support
            is_primary=False  # Default value, adjust as needed
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        logger.info(f"Address {new_address.id} created successfully for user {user_id}")
        return new_address
    except HTTPException as http_err:
        # Catch and log user validation errors
        logger.error(f"HTTP error during address creation for user {user_id}: {http_err.detail}")
        raise http_err
    except Exception as e:
        logger.error(f"Error creating address for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def get_address_by_id(db: Session, address_id: int):
    """
    Retrieve an address by its ID.
    """
    try:
        address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except Exception as e:
        logger.error(f"Error retrieving address {address_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def get_addresses_for_user(db: Session, user_id: int):
    """
    Retrieve all addresses for a user.
    Decoupled: Validates user through API.
    """
    try:
        # Validate user via user-service API
        validate_user(user_id)
        
        # Fetch addresses
        addresses = db.query(AddressModel).filter(AddressModel.user_id == user_id).all()
        logger.info(f"Query result for user {user_id}: {addresses}")
        if not addresses:
            logger.warning(f"No addresses found for user {user_id}")
        return addresses
    except Exception as e:
        logger.error(f"Error retrieving addresses for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def update_address(db: Session, db_address: AddressModel, address_update: AddressUpdate):
    """
    Update an address with the given address_update schema.
    """
    try:
        for key, value in address_update.dict(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        logger.info(f"Address {db_address.id} updated successfully")
        return db_address
    except Exception as e:
        logger.error(f"Error updating address {db_address.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def delete_address(db: Session, address_id: int):
    """
    Delete an address by its ID.
    """
    try:
        db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
        if db_address:
            db.delete(db_address)
            db.commit()
            logger.info(f"Address {address_id} deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Address not found")
        return db_address
    except Exception as e:
        logger.error(f"Error deleting address {address_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def set_primary_address(db: Session, address_id: int, user_id: int):
    """
    Set an address as the primary address for a user.
    """
    try:
        # Unset the current primary address
        db.query(AddressModel).filter(AddressModel.user_id == user_id, AddressModel.is_primary).update({"is_primary": False})
        
        # Set the new primary address
        address = db.query(AddressModel).filter(AddressModel.id == address_id, AddressModel.user_id == user_id).first()
        if address:
            address.is_primary = True
            db.commit()
            db.refresh(address)
            logger.info(f"Address {address_id} set as primary for user {user_id}")
            return address
        raise HTTPException(status_code=404, detail="Address not found")
    except Exception as e:
        logger.error(f"Error setting primary address {address_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

