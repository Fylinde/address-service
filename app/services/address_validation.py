import requests
import os
from fastapi import HTTPException

def validate_address_with_here_maps(address: str):
    api_key = os.getenv("HERE_MAPS_API_KEY", "")
    
    # Check if the API key is available
    if not api_key:
        raise HTTPException(status_code=500, detail="HERE Maps API key is missing")
    
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={api_key}"
    
    try:
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()
            
            # Check if we received any valid address items in the response
            if "items" in json_response and json_response["items"]:
                data = json_response["items"][0]  # Get the first result
                return True, {
                    "address": data["address"],
                    "position": data["position"]
                }
            else:
                return False, None
        else:
            # Handle failed request status codes
            raise HTTPException(status_code=response.status_code, detail="Error from HERE Maps API")
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions like timeouts, network issues, etc.
        raise HTTPException(status_code=500, detail=f"Error communicating with HERE Maps API: {str(e)}")
