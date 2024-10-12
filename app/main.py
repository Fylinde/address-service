# app/main.py
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.routes import address  # Import the new address routes
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from app.consumers.user_created_consumer import start_user_consuming  # Import the consumer
import logging
import threading

from starlette.middleware.errors import ServerErrorMiddleware


# Adjust log level globally
logging.basicConfig(level=logging.WARNING)  # Set to WARNING to reduce log output
logger = logging.getLogger(__name__)
# Adjust specific loggers
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)  # Reduce SQLAlchemy logs
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)    # Disable connection pool logs
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)      # Reduce Uvicorn logs

# Enable SQLAlchemy logging
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
#logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(address.router, prefix="/addresses", tags=["addresses"])
app.add_middleware(ServerErrorMiddleware, debug=True)

# Define the list of allowed origins explicitly
# Configure CORS
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Address Service!"}

# Start the user consumer for the address-service
def start_all_consumers():
    try:
        logger.info("Starting address-service user consumer...")
        user_thread = threading.Thread(target=start_user_consuming)
        user_thread.start()
        logger.info("Address-service user consumer started successfully.")
    except Exception as e:
        logger.error(f"Error while starting consumers: {str(e)}")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the Address Service...")
    start_all_consumers()
    logger.info("All consumers have been started.")
    
    
