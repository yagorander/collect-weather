from pydantic import BaseModel


class PostInput(BaseModel):
    request_id: int