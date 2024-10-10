from sqlalchemy.orm import Session

from models.user_models import User_Auth, User_Details
from schemas.user_schema import Create_User


def db_create_user(create_user_data: Create_User, db: Session):
    new_auth_user = User_Auth(
        username=create_user_data.username,
        password=create_user_data.password
    )
    db.add(new_auth_user)
    db.commit()
    db.refresh(new_auth_user)
    new_user_details = new_auth_user.dict()
    del new_user_details["password"]
    del new_user_details["username"]
    new_user_details = User_Details(**new_auth_user.dict(), user_auth_id=new_auth_user.user_id)
    db.add(new_user_details)
    db.commit()
    return new_user_details
