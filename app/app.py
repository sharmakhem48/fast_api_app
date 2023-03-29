from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from .database import engine,SessionLocal, Base
from sqlalchemy.orm import Session
from . import models
from .models import Address
from .schemas import Address, AddressUpdate
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine) # Create tables
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

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/get_address/{address_id}', status_code=status.HTTP_200_OK)
def get_address(address_id: int, response: Response, db: Session = Depends(get_db)):
    data = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not data:
        response.status_code = status.HTTP_404_NOT_FOUND
    return data


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

        




    




