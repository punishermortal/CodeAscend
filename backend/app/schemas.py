from pydantic import BaseModel

class LinkBase(BaseModel):
    url: str

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    id: int

    class Config:
        orm_mode = True
