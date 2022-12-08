from sqlalchemy import Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "tb_users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    city = Column(String)
    gender = Column(String)
    timestamp = Column(String)