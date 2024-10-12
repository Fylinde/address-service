from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import requests
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Assuming you have an endpoint in user-service to verify the token
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Fetch the current authenticated user by calling the user-service.
    This replaces the UserModel reference with an API call.
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{USER_SERVICE_URL}/me", headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        return response.json()  # Assuming user-service returns a JSON with user info

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="User service is unavailable") from e
