import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Category

app = FastAPI(title="Sneaker Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_doc(doc: dict) -> dict:
    doc = dict(doc)
    if doc.get("_id") is not None:
        doc["id"] = str(doc.pop("_id"))
    # Convert datetimes to isoformat if present
    for k, v in list(doc.items()):
        try:
            # datetime has isoformat
            if hasattr(v, "isoformat"):
                doc[k] = v.isoformat()
        except Exception:
            pass
    return doc


def seed_data_if_empty():
    if db is None:
        return
    # Seed categories
    if db["category"].count_documents({}) == 0:
        categories = [
            {
                "name": "Shoes",
                "slug": "shoes",
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1200"
            },
            {
                "name": "Clothing",
                "slug": "clothing",
                "image": "https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1200"
            },
            {
                "name": "Accessories",
                "slug": "accessories",
                "image": "https://images.unsplash.com/photo-1520975922284-9bcd8bdb1c46?q=80&w=1200"
            },
        ]
        for c in categories:
            create_document("category", Category(**c))
    # Seed products
    if db["product"].count_documents({}) == 0:
        products = [
            {
                "title": "Air Zoom Pegasus 40",
                "description": "Everyday responsive road running shoe.",
                "price": 129.99,
                "category": "Shoes",
                "brand": "Nike",
                "images": [
                    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1600"
                ],
                "colors": ["Black", "White", "Volt"],
                "sizes": ["7", "8", "9", "10", "11"],
                "rating": 4.7,
                "featured": True,
                "in_stock": True,
            },
            {
                "title": "Metcon 9",
                "description": "Stability and durability for lifting and HIIT.",
                "price": 149.99,
                "category": "Shoes",
                "brand": "Nike",
                "images": [
                    "https://images.unsplash.com/photo-1608231387042-66d1773070a5?q=80&w=1600"
                ],
                "colors": ["Grey", "Blue"],
                "sizes": ["6", "7", "8", "9", "10", "11", "12"],
                "rating": 4.6,
                "featured": True,
                "in_stock": True,
            },
            {
                "title": "Tech Fleece Hoodie",
                "description": "Premium warmth and modern fit.",
                "price": 110.00,
                "category": "Clothing",
                "brand": "Nike",
                "images": [
                    "https://images.unsplash.com/photo-1520974735194-2c1b3b2b0cda?q=80&w=1600"
                ],
                "colors": ["Black", "Olive"],
                "sizes": ["S", "M", "L", "XL"],
                "rating": 4.5,
                "featured": True,
                "in_stock": True,
            },
            {
                "title": "Club Cap",
                "description": "Classic cap with adjustable strap.",
                "price": 25.00,
                "category": "Accessories",
                "brand": "Nike",
                "images": [
                    "https://images.unsplash.com/photo-1609250291996-6a9bff2e43a8?q=80&w=1600"
                ],
                "colors": ["Black", "White", "Navy"],
                "sizes": ["One Size"],
                "rating": 4.3,
                "featured": False,
                "in_stock": True,
            },
        ]
        for p in products:
            create_document("product", Product(**p))


@app.get("/")
def read_root():
    return {"message": "Sneaker Store Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


@app.get("/api/categories")
def get_categories():
    seed_data_if_empty()
    docs = get_documents("category") if db is not None else []
    return [serialize_doc(d) for d in docs]


@app.get("/api/products")
def get_products(category: Optional[str] = None, featured: Optional[bool] = Query(None)):
    seed_data_if_empty()
    f = {}
    if category:
        f["category"] = category
    if featured is not None:
        f["featured"] = featured
    docs = get_documents("product", f or None) if db is not None else []
    return [serialize_doc(d) for d in docs]


@app.get("/api/products/featured")
def get_featured_products():
    return get_products(featured=True)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
