import requests
import json
import logging
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.utils.rabbitmq import RabbitMQConnection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_SERVICE_API_URL = 'http://user-service/api/users/'  # Replace with actual user-service API URL

def fetch_user_from_user_service(user_id):
    """
    Fetch user data from User-service.
    """
    try:
        response = requests.get(f"{USER_SERVICE_API_URL}{user_id}")
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching user from User-service: {e}")
        return None

def user_callback(ch, method, properties, body):
    user_data = json.loads(body)
    logger.info(f"Received user_created event for user_id: {user_data['id']}")

    db = SessionLocal()
    try:
        # Process user data and update Address-service database
        logger.info(f"Handling user data for user_id {user_data['id']} in Address-service")
        # Here, you would implement logic to update AddressModel or other models as required
        db.commit()
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except IntegrityError as e:
        logger.error(f"Database Integrity error: {str(e)}")
        db.rollback()
    except Exception as e:
        logger.error(f"Error processing user data: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_user_consuming():
    try:
        # Initialize RabbitMQ connection to subscribe to a specific queue
        rabbitmq = RabbitMQConnection(queue_name='user_verification_queue')
        
        logger.info("Starting to consume user_created events from user_verification_queue")
        rabbitmq.consume_messages(user_callback)

    except Exception as e:
        logger.error(f"Error while setting up consumer: {e}")

if __name__ == "__main__":
    start_user_consuming()
