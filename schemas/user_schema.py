from pydantic import BaseModel


class Create_User(BaseModel):
    username: str  # add email validation
    password: str
    first_name: str | None = None
    last_name: str | None = None


class Return_User(BaseModel):
    user_id: int
    username: str  # add email validation
    first_name: str | None = None
    last_name: str | None = None
    user_details_id: int
    verified: bool | None = None


class Return_User_With_Pwd(Return_User):
    password: str


class Authenticate_User(BaseModel):
    username: str
    password: str


class Notes_Schema(BaseModel):
    test_note: str


class Notes_Schema_response(BaseModel):
    id: int
    test_note: str
