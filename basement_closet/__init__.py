from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI

app = FastAPI()
data_store = {}

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    description: str
    age: Optional[int] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None
    location: Optional[str] = None


@app.put("/inventory")
def create(item: Item):
    data_store[item.id] = item
    return {"success": True, "item": item}


@app.get("/inventory")
def retrieve():
    return {"Hello": "World"}


@app.delete("/inventory/{item_id}")
def delete():
    return {"Hello": "World"}


@app.post("/inventory/comment/{item_id}")
def comment():
    return {"Hello": "World"}


@app.delete("/inventory/comment/{comment_id}")
def delete_comment():
    return {"Hello": "World"}
