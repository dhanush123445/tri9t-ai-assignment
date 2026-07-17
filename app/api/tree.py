from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.node import Node

router = APIRouter(
    prefix="/tree",
    tags=["Tree"]
)


def build_tree(node: Node, db: Session):
    """
    Recursively builds the JSON tree.
    """

    children = (
        db.query(Node)
        .filter(Node.parent_id == node.id)
        .order_by(Node.logical_id)
        .all()
    )

    return {
        "id": node.id,
        "logical_id": node.logical_id,
        "heading": node.heading,
        "level": node.level,
        "body": node.body,
        "content_hash": node.content_hash,
        "children": [
            build_tree(child, db)
            for child in children
        ]
    }


@router.get("/{version_id}")
def get_tree(
    version_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns the complete tree for one document version.
    """

    roots = (
        db.query(Node)
        .filter(
            Node.version_id == version_id,
            Node.parent_id == None
        )
        .order_by(Node.logical_id)
        .all()
    )

    return [
        build_tree(root, db)
        for root in roots
    ]


@router.get("/node/{node_id}")
def get_node(
    node_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns one node with children.
    """

    node = (
        db.query(Node)
        .filter(Node.id == node_id)
        .first()
    )

    if node is None:

        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    return build_tree(node, db)