from pydantic import BaseModel, Field
from uuid import uuid4
from typing import MutableMapping, Optional

from fastapi import FastAPI
from asyncmy import connect
from os import getenv

app = FastAPI()
data_store: MutableMapping[str, "Item"] = {}

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
    connection=await connect(
        user=getenv("DBUSER"),
        password=getenv("DBPWD"),
        host=getenv("DBHOST"),
        port=int(getenv("DBPORT")),
        database=getenv("DBNAME")
    )
    print("Connected to database")

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
