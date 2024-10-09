from pydantic import BaseModel


class Create_user_auth(BaseModel):
    email: str
    password: str


class Return_User_Auth(Create_user_auth):
    user_auth_id: int
    user_details_id: int

class Create_User_Details(BaseModel):
    first_name: str
    last_name: str
    verified: bool | None
    user_auth_id: int


class Notes_Schema(BaseModel):
    test_note: str


class Notes_Schema_response(BaseModel):
    id: int
    test_note: str




