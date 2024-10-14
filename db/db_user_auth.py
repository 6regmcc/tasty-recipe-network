from sqlalchemy.orm import Session

from models.user_models import User_Auth, User_Details
from schemas.user_schema import Create_User, Return_User, Return_User_With_Pwd


def db_create_user(create_user_data: Create_User, db: Session):
    new_auth_user = User_Auth(
        username=create_user_data.username,
        password=create_user_data.password
    )
    db.add(new_auth_user)
    db.commit()
    db.refresh(new_auth_user)

    new_user_details = User_Details(
        first_name=create_user_data.first_name,
        last_name=create_user_data.last_name,
        user_auth_id=new_auth_user.user_id
    )
    db.add(new_user_details)
    db.commit()
    return Return_User(**new_user_details.to_dict(), **new_auth_user.to_dict())


def db_get_user_by_username(username: str, db: Session):
    auth_user = db.query(User_Auth).filter(User_Auth.username == username).first()
    if auth_user is None:
        return False
    user_details = db_get_user_details_by_id(user_auth_id=auth_user.user_id, db=db)
    if user_details is None:
        return False
    return_user = Return_User_With_Pwd(**auth_user.to_dict(), **user_details.to_dict())

    return return_user


def db_get_user_details_by_id(user_auth_id: int, db: Session):
    user_details = db.query(User_Details).filter(User_Details.user_auth_id == user_auth_id).first()
    return user_details
