from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, open to all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/checkin", response_model=schemas.UserOut)
def checkin(username: str, db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, username)
    crud.check_in_today(db, user.id)
    return user

@app.get("/streak/{username}", response_model=schemas.StreakOut)
def get_streak(username: str, db: Session = Depends(get_db)):
    user = crud.get_or_create_user(db, username)
    return crud.calculate_streak(db, user.id)
