from sqlalchemy.orm import Session

from app.models.node import Node


class CompareService:

    @staticmethod
    def compare(db: Session, old_version_id: int, new_version_id: int):

        old_nodes = db.query(Node).filter(
            Node.version_id == old_version_id
        ).all()

        new_nodes = db.query(Node).filter(
            Node.version_id == new_version_id
        ).all()

        old_map = {
            node.logical_id: node
            for node in old_nodes
        }

        new_map = {
            node.logical_id: node
            for node in new_nodes
        }

        added = []
        removed = []
        modified = []
        unchanged = []

        # Detect added and modified
        for logical_id, new_node in new_map.items():

            if logical_id not in old_map:

                added.append({
                    "logical_id": logical_id,
                    "heading": new_node.heading
                })

            else:

                old_node = old_map[logical_id]

                if old_node.content_hash == new_node.content_hash:

                    unchanged.append({
                        "logical_id": logical_id,
                        "heading": new_node.heading
                    })

                else:

                    modified.append({
                        "logical_id": logical_id,
                        "heading": new_node.heading
                    })

        # Detect removed
        for logical_id, old_node in old_map.items():

            if logical_id not in new_map:

                removed.append({
                    "logical_id": logical_id,
                    "heading": old_node.heading
                })

        return {
            "added": added,
            "removed": removed,
            "modified": modified,
            "unchanged": unchanged,
            "summary": {
                "added": len(added),
                "removed": len(removed),
                "modified": len(modified),
                "unchanged": len(unchanged)
            }
        }