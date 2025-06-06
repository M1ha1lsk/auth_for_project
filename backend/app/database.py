from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
from passlib.context import CryptContext
from . import models

DATABASE_URL = "postgresql://auth_user:auth_password@db:5432/auth_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(db: Session):
    admin_user = db.query(models.User).filter(models.User.user_login == "admin").first()
    if not admin_user:
        admin = models.User(
            user_login="admin",
            user_role="admin",
            user_password=pwd_context.hash("admin_pwd")
        )
        db.add(admin)
        db.commit()

def get_user_by_login(db: Session, user_login: str):
    return db.query(models.User).filter(models.User.user_login == user_login).first()

def get_session_by_token(db: Session, session_token: str) -> Optional[object]:
    from .models import Session as UserSession
    return db.query(UserSession).filter(UserSession.session_token == session_token).first()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введенный пароль хешу"""
    return pwd_context.verify(plain_password, hashed_password)