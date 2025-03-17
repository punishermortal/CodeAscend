from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    description = Column(String)

class UserLinkStatus(Base):
    __tablename__ = "user_link_status"
    
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_solved = Column(Boolean, default=False)
    updated_on = Column(DateTime, default=datetime.utcnow)

    link = relationship("Link")
    user = relationship("User")
