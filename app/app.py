from fastapi import FastAPI, Depends, HTTPException, Request,Response
from .database import engine,SessionLocal, Base
from sqlalchemy.orm import Session
from . import models
from .models import Addresses
from .schemas import Address
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8082",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine) # Create tables

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/get_address/{address_id}')
def getaddress(address_id: int, db: Session = Depends(get_db)):
    return db.query(models.Addresses).filter(models.Addresses.id == address_id).first()


@app.post('/add_address')
async def insert_into_db(address: Address, db: Session = Depends(get_db)):
    address_model = models.Addresses()
    address_model.street = address.street
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.zip = address.zip
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    db.add(address_model)
    db.commit()
    return  address_model



    




