import hashlib

def create_hash(
        heading,
        body,
        level,
        parent_path
):

    text = (
        heading.strip()
        + body.strip()
        + str(level)
        + parent_path
    )

    return hashlib.sha256(
        text.encode()
    ).hexdigest()