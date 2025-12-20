from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI GitHub Actions Demo")

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "FastAPI is running with GitHub Actions!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/items")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
