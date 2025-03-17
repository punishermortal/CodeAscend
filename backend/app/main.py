from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from typing import List
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Logged in"}

@app.post("/links/", response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    # Only admin can add links
    return crud.create_link(db, link)

@app.get("/links/", response_model=List[schemas.Link])
def get_links(db: Session = Depends(get_db)):
    return crud.get_links(db)

@app.post("/userlinkstatus/", response_model=schemas.UserLinkStatus)
def update_user_link_status(user_link_status: schemas.UserLinkStatusCreate, db: Session = Depends(get_db)):
    return crud.update_link_status(db, user_link_status)
