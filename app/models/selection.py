from sqlalchemy import *

from app.db.database import Base

class Selection(Base):

    __tablename__="selections"

    id=Column(Integer,primary_key=True)

    name=Column(String)

    created_at=Column(DateTime,server_default=func.now())