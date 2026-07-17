from pydantic import BaseModel


class CompareRequest(BaseModel):
    old_version_id: int
    new_version_id: int