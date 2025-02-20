# BUILTIN modules
import uuid
from datetime import datetime
from typing import Optional

# Third party modules
from sqlmodel import SQLModel


class RetrieveInvoiceItemSchema(SQLModel):
    id: Optional[uuid.UUID]
    owner_id: Optional[int]
    absolute_id: Optional[str]
    invoice_id: Optional[uuid.UUID]
    product_id: Optional[uuid.UUID]
    product_price: Optional[float]
    quantity: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class RetrieveInvoiceSchema(SQLModel):
    id: Optional[uuid.UUID]
    absolute_id: Optional[str]
    owner_id: Optional[int]
    user_id: Optional[uuid.UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    total_price: Optional[float]
    address_id: Optional[uuid.UUID]
