# BUILTIN modules
import uuid
from datetime import date, datetime
from typing import Optional

import sqlalchemy as sa

# Third party modules
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlmodel import Field, SQLModel

# Local modules
###

"""
    Start Block Invoice Models
"""


class Invoices(SQLModel, table=True):
    __tablename__ = "invoices_invoice"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    absolute_id: str = Field(unique=False, nullable=False, max_length=128)
    owner_id: int = Field(unique=False, nullable=False)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True), ForeignKey("users_user.id", ondelete="CASCADE")
        )
    )
    total_price: float = Field(unique=False, nullable=False)
    address_id: Optional[uuid.UUID] = Field(
        sa_column=Column(
            UUID(as_uuid=True), ForeignKey("users_address.id", ondelete="CASCADE")
        )
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )


class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoices_invoiceItem"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    owner_id: int = Field(unique=False, nullable=False)
    absolute_id: str = Field(unique=False, nullable=False, max_length=128)
    invoice_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True), ForeignKey("invoices_invoice.id", ondelete="CASCADE")
        )
    )
    product_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True), ForeignKey("products_product.id", ondelete="CASCADE")
        )
    )
    product_price: Optional[float] = Field(unique=False, nullable=False)
    quantity: Optional[int] = Field(unique=False, nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )


"""
    End Block Invoice Models
"""

"""
    Start Block Product Models
"""


class Products(SQLModel, table=True):
    __tablename__ = "products_product"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    absolute_id: str = Field(unique=False, nullable=False, max_length=128)
    owner_id: int = Field(unique=False, nullable=False)
    price: Optional[float] = Field(unique=False, nullable=False)
    name: Optional[str] = Field(unique=False, nullable=False, max_length=128)
    state: Optional[str] = Field(unique=False, nullable=False, max_length=128)
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )


"""
    End Block Product Models
"""

"""
    Start Block User Models
"""


class User(SQLModel, table=True):
    __tablename__ = "users_user"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    absolute_id: str = Field(unique=False, nullable=False, max_length=128)
    owner_id: int = Field(unique=False, nullable=False)
    first_name: Optional[str] = Field(unique=False, nullable=False, max_length=128)
    last_name: Optional[str] = Field(unique=False, nullable=True, max_length=128)
    birthday: Optional[date] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )


class UserAddress(SQLModel, table=True):
    __tablename__ = "users_address"
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    absolute_id: str = Field(unique=False, nullable=False, max_length=128)
    owner_id: int = Field(unique=False, nullable=False)
    user_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True), ForeignKey("users_user.id", ondelete="CASCADE")
        )
    )
    city: Optional[str] = Field(unique=False, nullable=False, max_length=128)
    state: Optional[str] = Field(unique=False, nullable=False, max_length=128)
    address: Optional[str] = Field(unique=False, nullable=False, max_length=255)
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            onupdate=text("now()"),
        )
    )


"""
    End Block User Models
"""
