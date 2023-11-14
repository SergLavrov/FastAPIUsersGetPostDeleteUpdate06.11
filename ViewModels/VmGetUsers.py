from pydantic import BaseModel

class vm_get_users(BaseModel):
    id: int
    name: str
    lastName: str
    birthday: int
    city: str
    country: str
    eMail: str
