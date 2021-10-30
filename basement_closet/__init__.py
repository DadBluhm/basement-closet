from pydantic import BaseModel, Field
from uuid import uuid4
from typing import MutableMapping, Optional
import databases
import sqlalchemy
from fastapi import FastAPI

from os import getenv

app = FastAPI()
data_store: MutableMapping[str, "Item"] = {}

user=getenv("DBUSER")
password=getenv("DBPWD")
host=getenv("DBHOST")
port=int(getenv("DBPORT", "3306"))
dbname=getenv("DBNAME")

DATABASE_URL=f"mysql://{user}:{password}@{host}:{port}/{dbname}"
database=databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

inventory = sqlalchemy.Table(
    "inventory",
    metadata,
    sqlalchemy.Column("invID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("invName", sqlalchemy.String),
    sqlalchemy.Column("invType", sqlalchemy.String),
    sqlalchemy.Column("invDescription", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.String),
    sqlalchemy.Column("shelf", sqlalchemy.String),
    sqlalchemy.Column("bin", sqlalchemy.String),
    sqlalchemy.Column("location", sqlalchemy.String)
)

inventory_comments = sqlalchemy.Table(
    "inventory_comments",
    metadata,
    sqlalchemy.Column("invID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("commentID", sqlalchemy.String),
    sqlalchemy.Column("entryDate", sqlalchemy.DateTime),
    sqlalchemy.Column("enteredBy", sqlalchemy.String),
    sqlalchemy.Column("comment", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine, checkfirst=True)

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    description: str
    age: Optional[int] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None
    location: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    await database.connect()

    print("Connected to database")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.put("/inventory")
def create(item: Item):
    data_store[item.id] = item
    return {"success": True, "item": item}


@app.get("/inventory")
def retrieve(id: Optional[str] = None):
    if id:
        return {"results": [data_store[id]]}
    return {"results": list(data_store.values())}


@app.delete("/inventory/{item_id}")
def delete():
    return {"Hello": "World"}


@app.post("/inventory/comment/{item_id}")
def comment():
    return {"Hello": "World"}


@app.delete("/inventory/comment/{comment_id}")
def delete_comment():
    return {"Hello": "World"}
