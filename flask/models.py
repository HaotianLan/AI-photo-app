from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 用户表结构
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

# 创建数据库连接（SQLite）
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
