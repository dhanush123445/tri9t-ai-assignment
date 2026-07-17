from sqlalchemy.orm import Session

from app.models.selection import Selection
from app.models.selection_node import SelectionNode
from app.models.node import Node


class SelectionService:

    @staticmethod
    def create_selection(
        db: Session,
        name: str,
        version_id: int,
        node_ids: list[int]
    ):

        selection = Selection(
            name=name
        )

        db.add(selection)

        db.commit()

        db.refresh(selection)

        for node_id in node_ids:

            node = (
                db.query(Node)
                .filter(
                    Node.id == node_id
                )
                .first()
            )

            if node is None:
                continue

            item = SelectionNode(
                selection_id=selection.id,
                node_id=node.id,
                version_id=version_id
            )

            db.add(item)

        db.commit()

        return selection

    @staticmethod
    def get_selection(
        db: Session,
        selection_id: int
    ):

        return (
            db.query(Selection)
            .filter(
                Selection.id == selection_id
            )
            .first()
        )

    @staticmethod
    def get_selection_nodes(
        db: Session,
        selection_id: int
    ):

        return (
            db.query(SelectionNode)
            .filter(
                SelectionNode.selection_id == selection_id
            )
            .all()
        )