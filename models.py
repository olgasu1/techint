from sqlalchemy import Column, Integer, String
from db_config import ORMBaseModel
from pydantic import BaseModel

class Projector(ORMBaseModel):
    __tablename__ = 'projectors'
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, nullable=False)
    room_id = Column(Integer, index=True, nullable=False)

class ProjectorCreate(BaseModel):
    serial_number: str
    room_id: int

class SerialNumberUpdate(BaseModel):
    serial_number: str
