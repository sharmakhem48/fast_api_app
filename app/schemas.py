from pydantic import BaseModel, Field

class Address(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(min_length=1)
    country: str =  Field(min_length=1)
    zip: str =  Field(min_length=1)
    latitude: float
    longitude: float