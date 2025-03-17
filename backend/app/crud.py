from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_link(db: Session, link: schemas.LinkCreate):
    db_link = models.Link(url=link.url, description=link.description)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_links(db: Session):
    return db.query(models.Link).all()

def update_link_status(db: Session, user_link_status: schemas.UserLinkStatusCreate):
    db_status = db.query(models.UserLinkStatus).filter(
        models.UserLinkStatus.link_id == user_link_status.link_id,
        models.UserLinkStatus.user_id == user_link_status.user_id
    ).first()
    
    if db_status:
        db_status.is_solved = user_link_status.is_solved
        db_status.updated_on = datetime.utcnow()
    else:
        db_status = models.UserLinkStatus(
            link_id=user_link_status.link_id,
            user_id=user_link_status.user_id,
            is_solved=user_link_status.is_solved
        )
        db.add(db_status)
    
    db.commit()
    db.refresh(db_status)
    return db_status
