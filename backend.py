from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Offers API")

OFFERS = [
    {"id": 1, "title": "50% off shoes", "category": "fashion", "price": 50, "discount": 50, "rating": 4.5},
    {"id": 2, "title": "Discounted laptop", "category": "electronics", "price": 900, "discount": 10, "rating": 4.2},
    {"id": 3, "title": "Buy 1 Get 1 Free T-shirt", "category": "fashion", "price": 20, "discount": 50, "rating": 4.0},
    {"id": 4, "title": "Smartphone Sale", "category": "electronics", "price": 600, "discount": 15, "rating": 4.3},
]

class Offer(BaseModel):
    id: int
    title: str
    category: str
    price: float
    discount: float
    rating: float

@app.get("/offers", response_model=List[Offer])
async def get_offers(
    category: str = Query(None),
    max_price: float = Query(None),
    min_discount: float = Query(None),
    min_rating: float = Query(None)
):
    results = OFFERS
    if category:
        results = [o for o in results if o["category"] == category]
    if max_price is not None:
        results = [o for o in results if o["price"] <= max_price]
    if min_discount is not None:
        results = [o for o in results if o["discount"] >= min_discount]
    if min_rating is not None:
        results = [o for o in results if o["rating"] >= min_rating]
    return results
