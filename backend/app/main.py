from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List  # <-- Import List from typing
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a link
@app.post("/links/", response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db=db, link=link)

# Retrieve all links (fix: use List from typing)
@app.get("/links/", response_model=List[schemas.Link])  # <-- Correct here
def read_links(db: Session = Depends(get_db)):
    return crud.get_links(db=db)
