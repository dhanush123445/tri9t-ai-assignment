from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.compare import CompareRequest
from app.services.compare_service import CompareService

router = APIRouter(
    prefix="/compare",
    tags=["Compare"]
)


@router.post("/")
def compare_versions(
    request: CompareRequest,
    db: Session = Depends(get_db)
):
    """
    Compare two document versions and return
    added, removed, modified and unchanged nodes.
    """

    result = CompareService.compare(
        db=db,
        old_version_id=request.old_version_id,
        new_version_id=request.new_version_id
    )

    return result