import redis, os

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Get Redis connection details from environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

# Initialize Redis connection
rds = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, str]

@app.get("/")
def read_root():
    return {"Hello": "Worldss"}

@app.get("/hits")
def read_hits():
    rds.incr("hits")
    return {"number of hits": rds.get("hits")}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}