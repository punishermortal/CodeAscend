from sqlalchemy.orm import Session
from . import models, schemas

def create_link(db: Session, link: schemas.LinkCreate):
    db_link = models.Link(url=link.url)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_links(db: Session):
    return db.query(models.Link).all()
