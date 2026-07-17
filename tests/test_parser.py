from app.parser.hierarchy import parse_heading


def test_level():

    number, title, level = parse_heading(
        "2.1.1.1 Battery Life"
    )

    assert level == 4


def test_heading():

    number, title, level = parse_heading(
        "3.2 Cuff Inflation Sequence"
    )

    assert number == "3.2"

    assert title == "Cuff Inflation Sequence"