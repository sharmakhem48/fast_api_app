
from sqlalchemy import Column, Integer, String,Float
from .database import Base

class Addresses(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street: Column(String)
    city: Column(String)
    state: Column(String)
    country: Column(String)
    zip: Column(String)
    latitude: Column(Float)
    longitude: Column(Float)







