from dataclasses import dataclass, field

@dataclass
class ParsedNode:

    logical_id: str

    heading: str

    level: int

    body: str=""

    parent=None

    children: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    page:int=0

    hash:str=""