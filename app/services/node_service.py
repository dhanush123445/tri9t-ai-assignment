from sqlalchemy.orm import Session

from app.models.node import Node


class NodeService:
    """
    Handles saving and retrieving document tree nodes.
    """

    @staticmethod
    def save_tree(
        db: Session,
        version_id: int,
        parsed_nodes: list
    ):
        """
        Save an entire parsed tree.
        """

        for node in parsed_nodes:
            NodeService._save_node(
                db=db,
                version_id=version_id,
                parsed_node=node,
                parent_id=None
            )

        db.commit()

    @staticmethod
    def _save_node(
        db: Session,
        version_id: int,
        parsed_node,
        parent_id
    ):

        db_node = Node(
            version_id=version_id,
            logical_id=parsed_node.logical_id,
            parent_id=parent_id,
            heading=parsed_node.heading,
            level=parsed_node.level,
            body=parsed_node.body,
            content_hash=parsed_node.hash
        )

        db.add(db_node)
        db.flush()

        for child in parsed_node.children:

            NodeService._save_node(
                db=db,
                version_id=version_id,
                parsed_node=child,
                parent_id=db_node.id
            )

    @staticmethod
    def get_node(
        db: Session,
        node_id: int
    ):

        return (
            db.query(Node)
            .filter(Node.id == node_id)
            .first()
        )

    @staticmethod
    def get_children(
        db: Session,
        parent_id: int
    ):

        return (
            db.query(Node)
            .filter(Node.parent_id == parent_id)
            .order_by(Node.logical_id)
            .all()
        )

    @staticmethod
    def get_root_nodes(
        db: Session,
        version_id: int
    ):

        return (
            db.query(Node)
            .filter(
                Node.version_id == version_id,
                Node.parent_id == None
            )
            .order_by(Node.logical_id)
            .all()
        )

    @staticmethod
    def get_nodes_by_version(
        db: Session,
        version_id: int
    ):

        return (
            db.query(Node)
            .filter(Node.version_id == version_id)
            .order_by(Node.logical_id)
            .all()
        )

    @staticmethod
    def delete_version_nodes(
        db: Session,
        version_id: int
    ):

        (
            db.query(Node)
            .filter(Node.version_id == version_id)
            .delete()
        )

        db.commit()