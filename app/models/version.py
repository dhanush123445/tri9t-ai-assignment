from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Version(Base):

    __tablename__ = "versions"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    version_number = Column(Integer)

    uploaded_at = Column(
        DateTime,
        server_default=func.now()
    )