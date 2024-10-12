from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging
import traceback


# Enable logging
logging.basicConfig(level=logging.WARNING)

# SQLAlchemy engine setup with echo and stack trace
def log_query_stack_trace():
    stack = traceback.format_stack()
    logging.debug(''.join(stack))
    
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()

# Add event listener to log stack trace for every query
from sqlalchemy import event

#@event.listens_for(engine, "before_cursor_execute")
#def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
 #   logging.debug(f"Query: {statement}")
 #   log_query_stack_trace()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
