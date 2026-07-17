from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.selection import SelectionCreate
from app.services.selection_service import SelectionService

router = APIRouter(
    prefix="/selection",
    tags=["Selection"]
)


@router.post("/")
def create_selection(
    request: SelectionCreate,
    db: Session = Depends(get_db)
):

    selection = SelectionService.create_selection(
        db=db,
        name=request.name,
        version_id=request.version_id,
        node_ids=request.node_ids
    )

    return {
        "selection_id": selection.id,
        "name": selection.name
    }


@router.get("/{selection_id}")
def get_selection(
    selection_id: int,
    db: Session = Depends(get_db)
):

    selection = SelectionService.get_selection(
        db,
        selection_id
    )

    nodes = SelectionService.get_selection_nodes(
        db,
        selection_id
    )

    return {
        "selection_id": selection.id,
        "name": selection.name,
        "nodes": [
            {
                "node_id": n.node_id,
                "version_id": n.version_id
            }
            for n in nodes
        ]
    }