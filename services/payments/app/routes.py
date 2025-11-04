from fastapi import APIRouter, HTTPException, status
import logging
import uuid
from datetime import datetime

from app.models import PaymentCreate, Payment, PaymentStatus, RefundRequest
from app.database import get_database
from bson import ObjectId

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreate):
    """
    Create a payment transaction (stub implementation)
    In production, this would integrate with Stripe, PayPal, etc.
    """
    db = get_database()
    
    # Simulate payment processing
    transaction_id = f"txn_{uuid.uuid4().hex[:16]}"
    
    payment_dict = {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "payment_method": payment.payment_method,
        "status": PaymentStatus.PROCESSING,
        "transaction_id": transaction_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.payments.insert_one(payment_dict)
    
    # Simulate successful payment (in production, this would be async)
    await db.payments.update_one(
        {"_id": result.inserted_id},
        {"$set": {"status": PaymentStatus.COMPLETED, "updated_at": datetime.utcnow()}}
    )
    
    created_payment = await db.payments.find_one({"_id": result.inserted_id})
    
    logger.info(f"Payment created: {transaction_id} for order {payment.order_id}")
    
    return Payment(
        id=str(created_payment["_id"]),
        order_id=created_payment["order_id"],
        amount=created_payment["amount"],
        currency=created_payment["currency"],
        payment_method=created_payment["payment_method"],
        status=created_payment["status"],
        transaction_id=created_payment["transaction_id"],
        created_at=created_payment["created_at"],
        updated_at=created_payment["updated_at"]
    )

@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    """Get payment details by ID"""
    db = get_database()
    
    if not ObjectId.is_valid(payment_id):
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    
    payment = await db.payments.find_one({"_id": ObjectId(payment_id)})
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return Payment(
        id=str(payment["_id"]),
        order_id=payment["order_id"],
        amount=payment["amount"],
        currency=payment["currency"],
        payment_method=payment["payment_method"],
        status=payment["status"],
        transaction_id=payment.get("transaction_id"),
        created_at=payment["created_at"],
        updated_at=payment["updated_at"]
    )

@router.get("/payments/order/{order_id}", response_model=Payment)
async def get_payment_by_order(order_id: str):
    """Get payment details by order ID"""
    db = get_database()
    
    payment = await db.payments.find_one({"order_id": order_id})
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    
    return Payment(
        id=str(payment["_id"]),
        order_id=payment["order_id"],
        amount=payment["amount"],
        currency=payment["currency"],
        payment_method=payment["payment_method"],
        status=payment["status"],
        transaction_id=payment.get("transaction_id"),
        created_at=payment["created_at"],
        updated_at=payment["updated_at"]
    )

@router.post("/payments/refund")
async def refund_payment(refund: RefundRequest):
    """
    Refund a payment (stub implementation)
    In production, this would call the payment provider's refund API
    """
    db = get_database()
    
    if not ObjectId.is_valid(refund.payment_id):
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    
    payment = await db.payments.find_one({"_id": ObjectId(refund.payment_id)})
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if payment["status"] != PaymentStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Only completed payments can be refunded"
        )
    
    # Update payment status
    await db.payments.update_one(
        {"_id": ObjectId(refund.payment_id)},
        {"$set": {"status": PaymentStatus.REFUNDED, "updated_at": datetime.utcnow()}}
    )
    
    logger.info(f"Payment refunded: {payment['transaction_id']}")
    
    return {
        "message": "Payment refunded successfully",
        "payment_id": refund.payment_id,
        "amount_refunded": refund.amount or payment["amount"]
    }

@router.get("/payments/verify/{transaction_id}")
async def verify_payment(transaction_id: str):
    """
    Verify payment status by transaction ID
    Used by other services to confirm payment
    """
    db = get_database()
    
    payment = await db.payments.find_one({"transaction_id": transaction_id})
    
    if not payment:
        return {"verified": False, "status": None}
    
    return {
        "verified": payment["status"] == PaymentStatus.COMPLETED,
        "status": payment["status"],
        "payment_id": str(payment["_id"]),
        "amount": payment["amount"]
    }