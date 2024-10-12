from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

# Import your communication layer (e.g., requests for API, or RabbitMQ setup)

class AddressHistoryModel(BaseModel):
    __tablename__ = "address_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Removed ForeignKey to "users.id"
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    old_address = Column(String, nullable=False)  # Serialized version of the old address
    new_address = Column(String, nullable=False)  # Serialized version of the new address
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships with internal models only
    address = relationship("AddressModel", back_populates="address_history")

    def get_user_data(self):
        """ 
        Fetch user information from user-service via API or RabbitMQ.
        """
        # Example: Call an API to fetch user data
        # response = requests.get(f"http://user-service/api/users/{self.user_id}")
        # user_data = response.json()
        # return user_data

    def __repr__(self):
        return f"<AddressHistory user_id={self.user_id} address_id={self.address_id}>"
