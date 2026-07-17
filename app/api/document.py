
import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.parser.pdf_parser import PDFParser
from app.services.document_service import DocumentService
from app.services.node_service import NodeService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Validate file
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Save uploaded PDF
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create document
    document = DocumentService.create_document(
        db,
        file.filename
    )

    # Create version
    version = DocumentService.create_version(
        db,
        document.id
    )

    # Parse PDF
    parser = PDFParser(file_path)

    parsed_nodes = parser.parse()

    # Save parsed nodes
    NodeService.save_tree(
        db=db,
        version_id=version.id,
        parsed_nodes=parsed_nodes
    )

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "version_id": version.id,
        "root_nodes": len(parsed_nodes)
    }


@router.get("/")
def list_documents(
    db: Session = Depends(get_db)
):

    documents = DocumentService.get_all_documents(db)

    return [
        {
            "id": doc.id,
            "name": doc.name,
            "created_at": doc.created_at
        }
        for doc in documents
    ]


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = DocumentService.get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "id": document.id,
        "name": document.name,
        "created_at": document.created_at
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = DocumentService.get_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully."
    }