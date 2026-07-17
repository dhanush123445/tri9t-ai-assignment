from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.models.node import Node

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def search_nodes(
    q: str = Query(..., description="Search keyword"),
    version_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """
    Search headings and body text.
    """

    results = (
        db.query(Node)
        .filter(
            Node.version_id == version_id,
            or_(
                Node.heading.ilike(f"%{q}%"),
                Node.body.ilike(f"%{q}%")
            )
        )
        .order_by(Node.logical_id)
        .all()
    )

    return [
        {
            "id": node.id,
            "logical_id": node.logical_id,
            "heading": node.heading,
            "level": node.level,
            "body": node.body
        }
        for node in results
    ]