from pydantic import BaseModel, ConfigDict, Field


class SBookAdd(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int
    pages: int = Field(..., gt=10)
    is_read: bool = False


class SBook(SBookAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
