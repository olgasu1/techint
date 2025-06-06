from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from models import Projector, ProjectorCreate, SerialNumberUpdate
from db_config import ORMBaseModel, db_engine, get_db_session
from encoders import to_dict

ORMBaseModel.metadata.create_all(bind=db_engine)
app = FastAPI()

@app.get("/")
def test():
    return {"message": "Witoj chopie!"}

@app.post("/projectors")
def create_projector(projector_create: ProjectorCreate, db_session: Session = Depends(get_db_session)):
    new_projector = Projector(
        serial_number=projector_create.serial_number,
        room_id=projector_create.room_id
    )

    db_session.add(new_projector)
    db_session.commit()
    db_session.refresh(new_projector)
    
    return jsonable_encoder({
        "id": new_projector.id,
        "serial_number": new_projector.serial_number,
        "room_id": new_projector.room_id
    })

@app.get("/projectors")
def get_all_projectors(db_session: Session = Depends(get_db_session)):
    projectors = db_session.query(Projector).all()
    return jsonable_encoder([to_dict(projector) for projector in projectors])

@app.put("/projectors/{projector_id}/serial-number")
def update_serial_number(projector_id: int, serial_update: SerialNumberUpdate, db_session: Session = Depends(get_db_session)):
    projector = db_session.query(Projector).filter(Projector.id == projector_id).first()
    if not projector:
        raise HTTPException(status_code=404, detail="Projector not found")
    
    projector.serial_number = serial_update.serial_number
    db_session.commit()
    db_session.refresh(projector)

    return jsonable_encoder({
        "id": projector.id,
        "serial_number": projector.serial_number,
        "room_id": projector.room_id
    })