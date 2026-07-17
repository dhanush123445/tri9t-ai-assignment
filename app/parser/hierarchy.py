import re

heading_pattern = re.compile(
    r'^(\d+(\.\d+)*)\s+(.+)'
)

def is_heading(text):
    return bool(
        heading_pattern.match(text.strip())
    )

def parse_heading(text):

    m = heading_pattern.match(text.strip())

    if not m:
        return None

    number = m.group(1)

    title = m.group(3)

    # ↓ This is where the line belongs
    level = number.count(".") + 1

    return number, title, level