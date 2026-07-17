from sqlalchemy import *

from app.db.database import Base

class SelectionNode(Base):

    __tablename__="selection_nodes"

    id=Column(Integer,primary_key=True)

    selection_id=Column(Integer,ForeignKey("selections.id"))

    node_id=Column(Integer)

    version_id=Column(Integer)