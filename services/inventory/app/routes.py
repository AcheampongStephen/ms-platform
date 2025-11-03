from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
import logging

from app.models import ProductCreate, Product, ProductUpdate, StockCheck, StockReservation
from app.database import get_database
from bson import ObjectId
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    db = get_database()
    
    product_dict = product.model_dump()
    product_dict["created_at"] = datetime.utcnow()
    product_dict["updated_at"] = datetime.utcnow()
    product_dict["is_active"] = True
    product_dict["reserved_stock"] = 0
    
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    
    logger.info(f"Product created: {product.name}")
    
    return Product(
        id=str(created_product["_id"]),
        name=created_product["name"],
        description=created_product.get("description"),
        price=created_product["price"],
        category=created_product["category"],
        stock=created_product["stock"],
        image_url=created_product.get("image_url"),
        created_at=created_product["created_at"],
        is_active=created_product["is_active"],
        reserved_stock=created_product["reserved_stock"]
    )

@router.get("/products", response_model=List[Product])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None
):
    db = get_database()
    
    query = {"is_active": True}
    
    if category:
        query["category"] = category
    
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    
    cursor = db.products.find(query).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    return [
        Product(
            id=str(p["_id"]),
            name=p["name"],
            description=p.get("description"),
            price=p["price"],
            category=p["category"],
            stock=p["stock"],
            image_url=p.get("image_url"),
            created_at=p["created_at"],
            is_active=p["is_active"],
            reserved_stock=p.get("reserved_stock", 0)
        )
        for p in products
    ]

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return Product(
        id=str(product["_id"]),
        name=product["name"],
        description=product.get("description"),
        price=product["price"],
        category=product["category"],
        stock=product["stock"],
        image_url=product.get("image_url"),
        created_at=product["created_at"],
        is_active=product["is_active"],
        reserved_stock=product.get("reserved_stock", 0)
    )

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: ProductUpdate):
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    update_data = product_update.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return Product(
        id=str(product["_id"]),
        name=product["name"],
        description=product.get("description"),
        price=product["price"],
        category=product["category"],
        stock=product["stock"],
        image_url=product.get("image_url"),
        created_at=product["created_at"],
        is_active=product["is_active"],
        reserved_stock=product.get("reserved_stock", 0)
    )

@router.post("/products/{product_id}/check-availability", response_model=StockCheck)
async def check_availability(product_id: str, quantity: int = Query(..., gt=0)):
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    available_stock = product["stock"] - product.get("reserved_stock", 0)
    available = available_stock >= quantity
    
    return StockCheck(
        product_id=product_id,
        quantity=quantity,
        available=available
    )

@router.post("/products/{product_id}/reserve")
async def reserve_stock(reservation: StockReservation):
    db = get_database()
    
    if not ObjectId.is_valid(reservation.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(reservation.product_id)})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    available_stock = product["stock"] - product.get("reserved_stock", 0)
    
    if available_stock < reservation.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Reserve stock
    await db.products.update_one(
        {"_id": ObjectId(reservation.product_id)},
        {"$inc": {"reserved_stock": reservation.quantity}}
    )
    
    logger.info(f"Reserved {reservation.quantity} of product {reservation.product_id} for order {reservation.order_id}")
    
    return {"message": "Stock reserved successfully"}

@router.post("/products/{product_id}/release")
async def release_stock(reservation: StockReservation):
    db = get_database()
    
    if not ObjectId.is_valid(reservation.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Release stock
    await db.products.update_one(
        {"_id": ObjectId(reservation.product_id)},
        {"$inc": {"reserved_stock": -reservation.quantity}}
    )
    
    logger.info(f"Released {reservation.quantity} of product {reservation.product_id} for order {reservation.order_id}")
    
    return {"message": "Stock released successfully"}
