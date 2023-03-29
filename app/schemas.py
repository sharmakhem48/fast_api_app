from pydantic import BaseModel, validator
from typing import Optional


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    zip: str
    latitude: float
    longitude: float

    # Validate zip code bound to india only
    @validator('zip')
    def validate_zip(cls, v):
        if not v.isdigit() or len(v)!=6:
            raise ValueError('Invalid zip code- Bound to India only')
        return v



class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[int] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


