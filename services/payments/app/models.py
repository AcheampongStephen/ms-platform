from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"

class PaymentCreate(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: PaymentMethod

class PaymentInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    order_id: str
    amount: float
    currency: str
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Payment(BaseModel):
    id: str
    order_id: str
    amount: float
    currency: str
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RefundRequest(BaseModel):
    payment_id: str
    amount: Optional[float] = None  # If None, refund full amount
    reason: Optional[str] = None