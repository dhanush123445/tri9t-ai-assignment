from pydantic import BaseModel
from typing import List


class SelectionCreate(BaseModel):

    name: str

    version_id: int

    node_ids: List[int]