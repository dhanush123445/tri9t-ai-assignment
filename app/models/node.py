from sqlalchemy import *

from app.db.database import Base

class Node(Base):

    __tablename__="nodes"

    id=Column(Integer,primary_key=True)

    version_id=Column(Integer,ForeignKey("versions.id"))

    logical_id=Column(String)

    parent_id=Column(Integer,ForeignKey("nodes.id"))

    heading=Column(String)

    level=Column(Integer)

    body=Column(Text)

    content_hash=Column(String)