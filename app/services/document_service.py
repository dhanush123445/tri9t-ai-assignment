from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.version import Version


class DocumentService:
    """
    Handles creation of Documents and Versions.
    """

    @staticmethod
    def create_document(db: Session, name: str) -> Document:
        """
        Create a new document.
        """

        document = Document(
            name=name
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_document(db: Session, document_id: int):

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    @staticmethod
    def get_all_documents(db: Session):

        return db.query(Document).all()

    @staticmethod
    def create_version(
        db: Session,
        document_id: int
    ) -> Version:

        latest_version = (
            db.query(Version)
            .filter(
                Version.document_id == document_id
            )
            .order_by(
                Version.version_number.desc()
            )
            .first()
        )

        if latest_version:
            version_number = latest_version.version_number + 1
        else:
            version_number = 1

        version = Version(
            document_id=document_id,
            version_number=version_number
        )

        db.add(version)
        db.commit()
        db.refresh(version)

        return version

    @staticmethod
    def get_latest_version(
        db: Session,
        document_id: int
    ):

        return (
            db.query(Version)
            .filter(
                Version.document_id == document_id
            )
            .order_by(
                Version.version_number.desc()
            )
            .first()
        )

    @staticmethod
    def get_version(
        db: Session,
        version_id: int
    ):

        return (
            db.query(Version)
            .filter(
                Version.id == version_id
            )
            .first()
        )