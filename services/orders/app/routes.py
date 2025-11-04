from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import logging

from app.models import OrderCreate, Order, OrderUpdate, OrderStatus
from app.database import get_database
from bson import ObjectId
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Simple auth - in production, verify JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    # For now, just return a dummy user
    # In production, decode and verify JWT token
    return {"sub": "dummy_user_id"}

@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    user_id = current_user["sub"]
    
    # Calculate total
    total_amount = sum(item.price * item.quantity for item in order.items)
    
    # Create order
    order_dict = {
        "user_id": user_id,
        "items": [item.model_dump() for item in order.items],
        "shipping_address": order.shipping_address.model_dump(),
        "payment_method": order.payment_method,
        "status": OrderStatus.PENDING,
        "total_amount": total_amount,
        "tracking_number": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order_dict)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    
    logger.info(f"Order created: {result.inserted_id} for user {user_id}")
    
    return Order(
        id=str(created_order["_id"]),
        user_id=created_order["user_id"],
        items=[OrderItem(**item) for item in created_order["items"]],
        shipping_address=ShippingAddress(**created_order["shipping_address"]),
        payment_method=created_order["payment_method"],
        status=created_order["status"],
        total_amount=created_order["total_amount"],
        tracking_number=created_order.get("tracking_number"),
        created_at=created_order["created_at"],
        updated_at=created_order["updated_at"]
    )

@router.get("/orders", response_model=List[Order])
async def list_orders(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = current_user["sub"]
    
    cursor = db.orders.find({"user_id": user_id}).sort("created_at", -1)
    orders = await cursor.to_list(length=100)
    
    return [
        Order(
            id=str(o["_id"]),
            user_id=o["user_id"],
            items=[OrderItem(**item) for item in o["items"]],
            shipping_address=ShippingAddress(**o["shipping_address"]),
            payment_method=o["payment_method"],
            status=o["status"],
            total_amount=o["total_amount"],
            tracking_number=o.get("tracking_number"),
            created_at=o["created_at"],
            updated_at=o["updated_at"]
        )
        for o in orders
    ]

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify order belongs to user
    if order["user_id"] != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return Order(
        id=str(order["_id"]),
        user_id=order["user_id"],
        items=[OrderItem(**item) for item in order["items"]],
        shipping_address=ShippingAddress(**order["shipping_address"]),
        payment_method=order["payment_method"],
        status=order["status"],
        total_amount=order["total_amount"],
        tracking_number=order.get("tracking_number"),
        created_at=order["created_at"],
        updated_at=order["updated_at"]
    )

@router.put("/orders/{order_id}", response_model=Order)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify order belongs to user
    if order["user_id"] != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    update_data = order_update.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_data}
        )
    
    updated_order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    return Order(
        id=str(updated_order["_id"]),
        user_id=updated_order["user_id"],
        items=[OrderItem(**item) for item in updated_order["items"]],
        shipping_address=ShippingAddress(**updated_order["shipping_address"]),
        payment_method=updated_order["payment_method"],
        status=updated_order["status"],
        total_amount=updated_order["total_amount"],
        tracking_number=updated_order.get("tracking_number"),
        created_at=updated_order["created_at"],
        updated_at=updated_order["updated_at"]
    )

@router.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if order["status"] not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be cancelled at this stage"
        )
    
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": OrderStatus.CANCELLED, "updated_at": datetime.utcnow()}}
    )
    
    logger.info(f"Order cancelled: {order_id}")
    
    return {"message": "Order cancelled successfully"}