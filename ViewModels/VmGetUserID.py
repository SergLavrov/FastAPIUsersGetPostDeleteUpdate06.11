from pydantic import BaseModel

class vm_get_user_id(BaseModel):
    id: int
    name: str
    lastName: str
    birthday: int
    city: str
    country: str
    eMail: str