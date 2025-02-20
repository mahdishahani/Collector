# BUILTIN modules
from typing import Optional

# Third party modules
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel


class CreateInvoiceSchema(SQLModel):
    absolute_id: str
    owner_id: int
    user_id: UUID
    total_price: float
    address_id: Optional[UUID]


class CreateInvoiceItemSchema(SQLModel):
    absolute_id: str
    owner_id: int
    user_id: UUID
    product_id: UUID
    product_price: Optional[float]
    quantity: Optional[int]
