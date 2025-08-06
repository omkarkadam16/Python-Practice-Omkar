from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from StartUps.local_services_app.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship with bookings
    bookings = relationship("Booking", back_populates="user")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact = Column(String, nullable=False)

    # Relationship with bookings
    bookings = relationship("Booking", back_populates="provider")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    status = Column(String, default="Pending", nullable=False)

    # Relationships
    user = relationship("User", back_populates="bookings")
    provider = relationship("Provider", back_populates="bookings")
