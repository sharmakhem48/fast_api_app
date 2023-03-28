from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    zip: str
    latitude: float
    longitude: float


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[int] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
