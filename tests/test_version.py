from app.services.version_service import VersionService


class Dummy:

    def __init__(self, heading, body, content_hash, hash_value):
        self.heading = heading
        self.body = body
        self.content_hash = content_hash
        self.hash = hash_value


def test_similarity():

    score = VersionService.heading_similarity(
        "Battery Life",
        "Battery Life"
    )

    assert score == 100


def test_change_detection():

    old = Dummy(
        "Battery",
        "300 cycles",
        "abc",
        "abc"
    )

    new = Dummy(
        "Battery",
        "250 cycles",
        "abc",
        "xyz"
    )

    changed, unchanged = VersionService.detect_changes(
        [
            (old, new)
        ]
    )

    assert len(changed) == 1
    assert len(unchanged) == 0