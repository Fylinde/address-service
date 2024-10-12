from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import BaseModel

class AddressModel(BaseModel):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    company_name = Column(String(256), nullable=True)
    street_address_1 = Column(String(256), nullable=True)
    street_address_2 = Column(String(256), nullable=True)
    city = Column(String(256), nullable=True)
    city_area = Column(String(128), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(2), nullable=False)  # Assuming ISO country code
    country_area = Column(String(128), nullable=True)
    validation_skipped = Column(Boolean, default=False)
    state = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    phone_number = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)  # Removed ForeignKey to 'users.id'
    vendor_id = Column(Integer, nullable=True)  # Added support for multi-vendor addresses
    geolocation = Column(String, nullable=True)  # Field to store geolocation (lat,long) after validation
    address_type = Column(String, nullable=True)

    # Relationships with internal models only
    address_history = relationship("AddressHistoryModel", back_populates="address")

    def get_user_data(self):
        """ 
        Fetch user information from user-service via API or RabbitMQ.
        """
        # Example: Call an API to fetch user data
        # response = requests.get(f"http://user-service/api/users/{self.user_id}")
        # user_data = response.json()
        # return user_data

    def validate_address(self):
        """
        Implement address validation via external APIs (e.g., Google Maps API).
        """
        pass

    def __repr__(self):
        return f"<Address {self.street_address_1}, {self.city}, {self.country} ({self.address_type})>"
