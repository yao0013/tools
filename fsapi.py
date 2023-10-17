from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# 创建FastAPI应用
app = FastAPI()

# 创建数据库引擎和Session
DATABASE_URL = "mysql://root:gcloud123@localhost/hup"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库模型
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "title"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)



# 创建FastAPI端点
@app.get("/items/", response_model=list[Item])
def get_all_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
