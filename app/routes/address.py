from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.address_crud import (
    create_address, get_address_by_id, 
    get_addresses_for_user, update_address, delete_address
)
from app.schemas.address_schemas import AddressCreate, AddressUpdate, AddressResponse
from app.auth.auth import get_current_user
from app.services.address_validation import validate_address_with_here_maps  # Import address validation service
import os
import requests
import logging
from typing import List
from app.models.address import AddressModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Route for creating a new address
@router.post("/addresses", response_model=AddressResponse)
def create_new_address(
    address: AddressCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Updated: current_user is now a dict from user-service API
):
    try:
        user_id = current_user['id']  # Extract user ID from the API response
        logger.info(f"User {user_id} is creating a new address")
        
        # Validate address using HERE Maps API
        valid, data = validate_address_with_here_maps(f"{address.street}, {address.city}, {address.state}, {address.country}")
        logger.info(f"Address validation result: {valid}, data: {data}")
        
        if not valid:
            logger.warning(f"Address validation failed for user {user_id}: {address.street}, {address.city}, {address.state}, {address.country}")
            raise HTTPException(status_code=400, detail="Invalid address")

        # Proceed with creating the address in the database
        new_address = create_address(db, address, user_id=user_id)
        logger.info(f"Address created successfully for user {user_id}: {new_address.id}")
        
        return new_address

    except HTTPException as http_err:
        logger.error(f"HTTP error while creating address for user {user_id}: {str(http_err)}")
        raise http_err

    except Exception as e:
        logger.error(f"Unexpected error while creating address for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


# Route for fetching a single address by its ID
@router.get("/addresses/id/{address_id}", response_model=AddressResponse)
def get_address_by_id_route(
    address_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Updated: current_user is now a dict from user-service API
):
    user_id = current_user['id']
    address = get_address_by_id(db, address_id)
    
    # Ensure that the user fetching the address is the one who owns it
    if not address or address.user_id != user_id:
        logger.warning(f"User {user_id} attempted to access address {address_id} which they do not own.")
        raise HTTPException(status_code=404, detail="Address not found")
    
    logger.info(f"Address {address_id} retrieved successfully for user {user_id}")
    return address


@router.get("/users/{user_id}/addresses", response_model=List[AddressResponse])
def get_user_addresses(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Updated: current_user is now a dict from user-service API
):
    try:
        current_user_id = current_user['id']
        logger.info(f"Fetching addresses for user_id: {user_id}")
        if current_user_id != user_id:
            logger.warning(f"Unauthorized attempt by user {current_user_id} to access addresses of user {user_id}")
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")
        
        addresses = db.query(AddressModel).filter(AddressModel.user_id == user_id).all()

        if not addresses:
            logger.info(f"No addresses found for user {user_id}")
            raise HTTPException(status_code=404, detail="No addresses found")

        logger.info(f"Addresses retrieved for user {user_id}: {len(addresses)} found")
        return addresses
    except Exception as e:
        logger.error(f"Error while fetching addresses for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Route for updating an existing address
@router.put("/addresses/{address_id}", response_model=AddressResponse)
def update_existing_address(
    address_id: int, 
    address_update: AddressUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Updated: current_user is now a dict from user-service API
):
    user_id = current_user['id']
    address = get_address_by_id(db, address_id)
    
    if not address or address.user_id != user_id:
        logger.warning(f"User {user_id} tried to update address {address_id} they do not own.")
        raise HTTPException(status_code=404, detail="Address not found")

    # Validate address using HERE Maps API before updating
    valid, data = validate_address_with_here_maps(f"{address_update.street}, {address_update.city}, {address_update.state}, {address_update.country}")
    if not valid:
        logger.warning(f"Address validation failed for update by user {user_id}: {address_update}")
        raise HTTPException(status_code=400, detail="Invalid address")

    updated_address = update_address(db, address, address_update)
    logger.info(f"Address {address_id} updated successfully by user {user_id}")
    return updated_address

# Route for deleting an existing address
@router.delete("/addresses/{address_id}")
def delete_existing_address(
    address_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Updated: current_user is now a dict from user-service API
):
    user_id = current_user['id']
    
    # Fetch the address to be deleted
    address = get_address_by_id(db, address_id)

    # Ensure that the user owns the address
    if not address or address.user_id != user_id:
        logger.warning(f"User {user_id} tried to delete address {address_id} they do not own.")
        raise HTTPException(status_code=404, detail="Address not found")

    # Fetch all addresses for the user
    user_addresses = db.query(AddressModel).filter(AddressModel.user_id == user_id).all()

    # Check if the user only has one address
    if len(user_addresses) == 1:
        logger.warning(f"User {user_id} tried to delete their only address {address_id}.")
        raise HTTPException(status_code=400, detail="You cannot delete your only address. Please add a new address before deleting this one.")

    # Check if the address to be deleted is the default (primary) address
    if address.is_primary:
        # Check if there are other addresses available to promote to default
        secondary_addresses = [addr for addr in user_addresses if addr.id != address_id]
        
        if not secondary_addresses:
            logger.warning(f"User {user_id} tried to delete their default address {address_id} with no other addresses available.")
            raise HTTPException(status_code=400, detail="You cannot delete your default address without setting another address as default first.")
        
        # Promote the first secondary address to default
        new_default_address = secondary_addresses[0]
        new_default_address.is_primary = True
        db.commit()
        logger.info(f"Address {new_default_address.id} promoted to default for user {user_id}.")

    # Proceed with deletion if the address is not the only address and not the default
    delete_address(db, address_id)
    logger.info(f"Address {address_id} deleted successfully by user {user_id}")
    return {"detail": "Address deleted"}
