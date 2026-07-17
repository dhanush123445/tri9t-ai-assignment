from rapidfuzz import fuzz


class VersionService:

    SIMILARITY_THRESHOLD = 85

    @staticmethod
    def heading_similarity(a, b):
        return fuzz.ratio(a.lower(), b.lower())

    @staticmethod
    def body_similarity(a, b):
        return fuzz.ratio(a.lower(), b.lower())

    @staticmethod
    def match_nodes(old_nodes, new_nodes):

        matched = []
        unmatched = []

        for new_node in new_nodes:

            best_score = 0
            best_node = None

            for old_node in old_nodes:

                score = VersionService.heading_similarity(
                    old_node.heading,
                    new_node.heading
                )

                if score > best_score:
                    best_score = score
                    best_node = old_node

            if (
                best_node is not None
                and best_score >= VersionService.SIMILARITY_THRESHOLD
            ):
                matched.append((best_node, new_node))
            else:
                unmatched.append(new_node)

        return matched, unmatched

    @staticmethod
    def detect_changes(matched_nodes):

        changed = []
        unchanged = []

        for old_node, new_node in matched_nodes:

            if old_node.content_hash == new_node.hash:
                unchanged.append(new_node)
            else:
                changed.append((old_node, new_node))

        return changed, unchanged

    @staticmethod
    def diff_summary(old_node, new_node):

        summary = []

        if old_node.heading != new_node.heading:
            summary.append("Heading changed")

        if old_node.body != new_node.body:
            summary.append("Body changed")

        return summary