from sqlalchemy.orm import Session
from . import models
from datetime import date, timedelta

def get_or_create_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        user = models.User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def check_in_today(db: Session, user_id: int):
    today = date.today()
    checkin = db.query(models.CheckIn).filter_by(user_id=user_id, date=today).first()
    if not checkin:
        db.add(models.CheckIn(user_id=user_id, date=today))
        db.commit()

def calculate_streak(db: Session, user_id: int):
    checkins = db.query(models.CheckIn).filter_by(user_id=user_id).order_by(models.CheckIn.date.desc()).all()

    current_streak = 0
    longest_streak = 0
    streak = 0
    last_date = None

    for c in checkins:
        if last_date is None:
            streak = 1
        else:
            if (last_date - c.date).days == 1:
                streak += 1
            elif (last_date - c.date).days == 0:
                continue  # Same day, skip
            else:
                streak = 1
        last_date = c.date
        longest_streak = max(longest_streak, streak)

    if checkins and checkins[0].date == date.today():
        current_streak = streak
    else:
        current_streak = 0

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    }
