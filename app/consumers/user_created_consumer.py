import pika
import json
import logging
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models.user import UserModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def user_callback(ch, method, properties, body):
    user_data = json.loads(body)

    logger.info(f"Received user_created event for user_id: {user_data['id']}")

    db = SessionLocal()
    try:
        # Check if the user already exists in the address-service
        existing_user = db.query(UserModel).filter(UserModel.id == user_data["id"]).first()
        if existing_user:
            logger.info(f"User with id {user_data['id']} already exists in address-service.")
        else:
            logger.info(f"Adding new user with id {user_data['id']} to address-service.")
            new_user = UserModel(
                id=user_data["id"],
                full_name=user_data.get("full_name"),
                email=user_data["email"],
                phone_number=user_data.get("phone_number"),
                hashed_password=user_data.get("hashed_password"),
                is_active=user_data.get("is_active", True),
                is_admin=user_data.get("is_admin", False)
            )
            db.add(new_user)
            db.commit()
            logger.info(f"User {new_user.full_name} (ID: {new_user.id}) added to address-service.")
    except IntegrityError as e:
        logger.error(f"Integrity error occurred: {str(e)}")
        db.rollback()
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        db.rollback()
    finally:
        db.close()


def start_user_consuming():
    logger.info("Connecting to RabbitMQ for user creation messages")
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    
    channel = connection.channel()

    # Declare the exchange that will be used to receive user events
    channel.exchange_declare(exchange='user_events', exchange_type='fanout')
    logger.info("Exchange 'user_events' declared")

    # Create an exclusive queue for the address-service consumer
    queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
    channel.queue_bind(exchange='user_events', queue=queue_name)
    logger.info(f"Queue {queue_name} bound to exchange 'user_events'")

    logger.info("Waiting for user messages. To exit press CTRL+C")

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=user_callback, auto_ack=True)
    channel.start_consuming()
