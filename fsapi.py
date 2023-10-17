from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# 创建FastAPI应用
app = FastAPI()

# 创建数据库引擎和Session
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库模型
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建Pydantic模型来定义API返回的数据格式
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

# 创建FastAPI端点
@app.get("/items/", response_model=list[ItemResponse])
def get_all_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items
