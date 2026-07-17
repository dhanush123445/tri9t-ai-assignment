from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Document(Base):

    __tablename__="documents"

    id=Column(Integer,primary_key=True)

    name=Column(String,nullable=False)

    created_at=Column(DateTime,server_default=func.now())