from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class StreakOut(BaseModel):
    current_streak: int
    longest_streak: int
