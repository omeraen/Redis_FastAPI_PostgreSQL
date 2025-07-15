import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import redis

load_dotenv()

DB = os.getenv("DB")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

engine = create_engine(DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + Redis + Postgres Demo")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/items/nocache")
def get_items_no_cache(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {"data": items, "cached": False}

@app.get("/items/cache")
def get_items_cache(db: Session = Depends(get_db)):
    cached_items = r.get("items_cache")
    if cached_items:
        return {"data": eval(cached_items), "cached": True}
    items = db.query(Item).all()
    items_data = [{"id": item.id, "name": item.name} for item in items]
    r.set("items_cache", str(items_data))
    return {"data": items_data, "cached": False}

@app.post("/items")
def create_item(name: str, db: Session = Depends(get_db)):
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    r.delete("items_cache")
    return {"created_id": new_item.id, "name": new_item.name} 
