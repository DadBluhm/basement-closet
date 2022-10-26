from pydantic import BaseModel, Field
from typing import MutableMapping, Optional
import databases
import sqlalchemy
from fastapi import FastAPI
from datetime import datetime

from os import getenv

from sqlalchemy.sql.schema import ForeignKey

app = FastAPI()
data_store: MutableMapping[str, "Item"] = {}

user = getenv("DBUSER")
password = getenv("DBPWD")
host = getenv("DBHOST")
port = int(getenv("DBPORT", "3306"))
dbname = getenv("DBNAME")

DATABASE_URL = f"mysql+mariadbconnector://{user}:{password}@{host}:{port}/{dbname}"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

inventory = sqlalchemy.Table(
    "inventory",
    metadata,
    sqlalchemy.Column("invID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("invName", sqlalchemy.String(30)),
    sqlalchemy.Column("invType", sqlalchemy.String(30)),
    sqlalchemy.Column("invDescription", sqlalchemy.String(512)),
    sqlalchemy.Column("age", sqlalchemy.String(30)),
    sqlalchemy.Column("shelf", sqlalchemy.String(30)),
    sqlalchemy.Column("bin", sqlalchemy.String(30)),
    sqlalchemy.Column("location", sqlalchemy.String(30)),
    sqlalchemy.Column("useful", sqlalchemy.Boolean),
)

inventory_comments = sqlalchemy.Table(
    "inventory_comments",
    metadata,
    sqlalchemy.Column("commentID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "invID", sqlalchemy.Integer, ForeignKey("inventory.invID"), primary_key=True
    ),
    sqlalchemy.Column("entryDate", sqlalchemy.DateTime),
    sqlalchemy.Column("enteredBy", sqlalchemy.String(30)),
    sqlalchemy.Column("comment", sqlalchemy.String(512)),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine, checkfirst=True)


class ItemIn(BaseModel):
    name: str = Field(alias="invName")
    type: str = Field(alias="invType")
    description: str = Field(alias="invDescription")
    age: Optional[int] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None
    location: Optional[str] = None
    useful: bool = False


class Item(ItemIn):
    id: int = Field(alias="invID")


@app.on_event("startup")
async def startup_event():
    await database.connect()
    print("Connected to database")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.put("/inventory")
async def create(item: ItemIn):
    query = inventory.insert().values(**item.dict(by_alias=True))
    inserted_id = await database.execute(query)
    inserted_item = Item(**{"invID": inserted_id, **item.dict(by_alias=True)})
    return {"success": True, "item": inserted_item}


@app.get("/inventory")
async def retrieve(id: Optional[str] = None):
    if id:
        query = inventory.select(inventory.c.invID == id)
    else:
        query = inventory.select()
    return {"results": await database.fetch_all(query)}


@app.get("/inventory/{item_id}")
async def get_item(item_id: str):
    query = inventory.select(inventory.c.invID == item_id)
    return {"result": await database.fetch_one(query)}


@app.delete("/inventory/{item_id}")
async def delete(item_id: str):
    query = inventory.delete(inventory.c.invID == item_id)
    await database.execute(query)
    return {"success": True}


class CommentIn(BaseModel):
    entry_date: Optional[datetime] = Field(
        alias="entryDate", default_factory=lambda: datetime.now()
    )
    entered_by: str = Field(alias="enteredBy")
    comment: str


class Comment(CommentIn):
    inv_id: int = Field(alias="invID")
    id: int = Field(alias="commentID")


@app.post("/inventory/comment/{item_id}")
async def comment(item_id: str, comment: CommentIn):
    query = inventory_comments.insert().values(
        invID=item_id, **comment.dict(by_alias=True)
    )
    inserted_id = await database.execute(query)
    return {
        "success": True,
        "comment": Comment(
            **{"invID": item_id, "commentID": inserted_id},
            **comment.dict(by_alias=True),
        ),
    }


@app.get("/inventory/comment/{item_id}")
async def get_comments(item_id: str):
    query = inventory_comments.select(inventory_comments.c.invID == item_id)
    return {"results": await database.fetch_all(query)}


@app.delete("/inventory/comment/{comment_id}")
async def delete_comment():
    return {"Hello": "World"}
