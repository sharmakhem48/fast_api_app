from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from .database import engine,SessionLocal, engine
from sqlalchemy.orm import Session
from . import models
from .models import Address
from .schemas import Address, AddressUpdate
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .backend import closest_places_ids
import sqlite3
import logging

models.Base.metadata.create_all(bind=engine) # Create tables
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8002",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/get_address/{latitude}/{longitude}', status_code=status.HTTP_200_OK)
async def get_address(latitude: str, longitude: str, response: Response, db: Session = Depends(get_db)):
    conn = sqlite3.connect("fast_api_app.db")
    cursor = conn.cursor()
    sql= f'''SELECT * FROM addresses WHERE latitude BETWEEN cast({latitude} as float) AND cast({latitude} as float)+1 AND longitude BETWEEN cast({longitude} as float) AND cast({longitude} as float)+1
            '''
    print(sql)
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in data]
        data = pd.DataFrame(data)
        address_id = closest_places_ids(data, latitude, longitude)
        data = data.loc[data['id'].isin(address_id)]
        if data.empty:
            response.status_code = status.HTTP_404_NOT_FOUND
    finally:
        cursor.close()
        conn.close()
    return data.to_dict()


@app.post('/add_address',  status_code=status.HTTP_201_CREATED)
async def create_address(address: Address, response: Response, db: Session = Depends(get_db)):
    try:
        address_model = models.Address()
        address_model.street = address.street
        address_model.city = address.city
        address_model.state = address.state
        address_model.country = address.country
        address_model.zip = address.zip
        address_model.latitude = address.latitude
        address_model.longitude = address.longitude
        db.add(address_model)
        db.commit()
        db.refresh(address_model)
        return  {'address_id':address_model.id}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'Message':f"Cannot add address :{e}"}


@app.delete('/delete_address/{address_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, 
                   response: Response, db: Session = Depends(get_db)):
    data = db.query(models.Address).filter(models.Address.id==address_id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address_id - {address_id} not found" )
    data.delete(synchronize_session=False)
    db.commit()
    return {'Message':f"Address_id - {address_id} deleted successfully"}

    
@app.patch('/update_address/{address_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_address(address_id: int, request: AddressUpdate 
                   , response: Response, db: Session = Depends(get_db)):

    data = db.query(models.Address).filter(models.Address.id==address_id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address_id {address_id} not found" )
    request_dict = request.dict(exclude_unset=True)
    data.update(request_dict)
    db.commit()
    return {'Message':f"Record updated for address_id : {address_id}"}

        




    




