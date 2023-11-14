from pydantic import BaseModel

class vm_add_user(BaseModel):
    id: int
    name: str
    lastName: str
    birthday: int
    city: str
    country: str
    eMail: str
