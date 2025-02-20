# Third party modules
from typing import Any

from loguru import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Local modules
from ..repository.data_adapter import DataOperationsRepository
from ..repository.db import async_engine
from ..repository.models import InvoiceItem, Invoices, Products, User, UserAddress

ALL_STATUS = ["invoices__paid"]


class MessageResponseLogic:
    """
    This class implements the Collector business logic layer
    for RabbitMQ response messages.
    """

    def __init__(self, repository: DataOperationsRepository):
        """The class initializer.

        :param repository: Data layer handler object.
        """
        self.repo = repository

    async def _paid_invoice_and_save_to_db(self, message):
        #  TODO Save New Invoice To DB
        data = message.get("body", "")
        if not data:
            logger.critical(f"Data for create : {Invoices} not found")
            return
        # get other data from message
        owner_id = data.pop("owner_id", False)
        invoice_data = data.pop("invoice_data", False)
        item_list_data = False
        if invoice_data:
            user_id = invoice_data.get("user_id", False)
            address_id = invoice_data.get("address_id", False)
            item_list_data = invoice_data.pop("list_item", False)
            if user_id:
                user_recognize = await self._recognize_user_id(user_id, owner_id)
            else:
                logger.critical(
                    f"user id is required in Invoice => {invoice_data.get('id')}"
                )
                return
            if address_id:
                address_recognize = await self._recognize_address_id(
                    address_id, owner_id
                )
            else:
                logger.critical(
                    f"user id is required in Invoice => {invoice_data.get('id')}"
                )
                return
        try:
            # crate instance for save new Invoices
            new_invoices = Invoices(
                absolute_id=invoice_data["id"],
                owner_id=owner_id,
                user_id=user_recognize.id,
                address_id=address_recognize.id,
                total_price=invoice_data["total_price"],
            )
            # Call the _write method of the repository to perform database write
            invoices_obj = await self.repo._write(model_instance=new_invoices)
        except Exception as e:
            logger.critical(f"Failed to save data to DB Invoices: => {e}")
            return

        # conditional for save InvoiceItem
        if item_list_data:
            await self._save_invoice_item_by_invoice_obj(
                item_data=item_list_data, invoices=invoices_obj
            )
        else:
            logger.critical(
                f"user id is required in Invoice => {invoice_data.get('id')}"
            )

    async def _recognize_user_id(self, user_id, owner_id):
        try:
            async with AsyncSession(async_engine) as db:
                query = select(User).where(
                    User.absolute_id == str(user_id), User.owner_id == owner_id
                )
                result = await db.exec(query)
                user_obj = result.one()
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy errors
            logger.critical(
                f"SQLAlchemy Error for get user in _recognize_user_id: {sql_err}"
            )
            await db.rollback()

        except IntegrityError as integrity_err:
            # Handle integrity constraint violations
            logger.critical(
                f"Integrity Error for get user in _recognize_user_id: {integrity_err}"
            )
            await db.rollback()
        except Exception as e:
            # Handle other exceptions
            logger.critical(
                f"Failed processing for get user in _recognize_user_id response => {e}"
            )
            await db.rollback()
        if user_obj:
            return user_obj
        else:
            model_instance = User(absolute_id=user_id, owner_id=owner_id)
            create_query = await self.repo._write(model_instance=model_instance)
            if create_query:
                return create_query
            else:
                logger.critical("Failed to create model  => User")

    async def _recognize_address_id(self, address_id, owner_id):
        try:
            async with AsyncSession(async_engine) as db:
                query = select(UserAddress).where(
                    UserAddress.absolute_id == str(address_id),
                    UserAddress.owner_id == owner_id,
                )
                result = await db.exec(query)
                address_obj = result.one()
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy errors
            logger.critical(
                f"SQLAlchemy Error for get user in _recognize_address_id: {sql_err}"
            )
            await db.rollback()

        except IntegrityError as integrity_err:
            # Handle integrity constraint violations
            logger.critical(
                f"Integrity Error for get user in _recognize_address_id: {integrity_err}"
            )
            await db.rollback()
        except Exception as e:
            # Handle other exceptions
            logger.critical(
                f"Failed processing for get user in _recognize_address_id response => {e}"
            )
            await db.rollback()
        if address_obj:
            return address_obj
        else:
            model_instance = UserAddress(absolute_id=address_id, owner_id=owner_id)
            create_query = await self.repo._write(model_instance=model_instance)
            if create_query:
                return create_query
            else:
                logger.critical("Failed to create model  => UserAddress")

    async def _recognize_product_id(self, product_id, owner_id):
        try:
            async with AsyncSession(async_engine) as db:
                query = select(Products).where(
                    Products.absolute_id == str(product_id),
                    Products.owner_id == owner_id,
                )
                result = await db.exec(query)
                product_obj = result.one()
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy errors
            logger.critical(
                f"SQLAlchemy Error for get user in _recognize_address_id: {sql_err}"
            )
            await db.rollback()

        except IntegrityError as integrity_err:
            # Handle integrity constraint violations
            logger.critical(
                f"Integrity Error for get user in _recognize_address_id: {integrity_err}"
            )
            await db.rollback()
        except Exception as e:
            # Handle other exceptions
            logger.critical(
                f"Failed processing for get user in _recognize_address_id response => {e}"
            )
            await db.rollback()
        if product_obj:
            return product_obj
        else:
            model_instance = Products(absolute_id=product_id, owner_id=owner_id)
            create_query = await self.repo._write(model_instance=model_instance)
            if create_query:
                return create_query
            else:
                logger.critical("Failed to create model  => Products")

    async def _save_invoice_item_by_invoice_obj(
        self, item_data: list, invoices: Any, owner_id
    ):
        for data in item_data:
            product_id = data.pop("product_id", False)
            if product_id:
                product_recognize = await self._recognize_product_id(
                    product_id, owner_id
                )
                # crate instance for save new Invoices Item
                new_invoice_item = InvoiceItem(
                    absolute_id=data["id"],
                    owner_id=owner_id,
                    invoice_id=invoices.id,
                    product_id=product_recognize.id,
                    product_price=data["product_price"],
                    quantity=data["quantity"],
                )
                # Call the _write method of the repository to perform database write
                await self.repo._write(model_instance=new_invoice_item)
            else:
                # crate instance for save new Invoices Item
                new_invoice_item = InvoiceItem(
                    absolute_id=data["id"],
                    owner_id=owner_id,
                    invoice_id=invoices.id,
                    roduct_price=data["product_price"],
                    quantity=data["quantity"],
                )
                # Call the _write method of the repository to perform database write
                await self.repo._write(model_instance=new_invoice_item)

    async def process_response(self, message: dict):
        """Process response message data.
        Implemented business logic:
          - Every received message state is updated in DB.
        :param message: Response message data.
        """
        status = message["status"]
        try:
            if status not in ALL_STATUS:
                raise RuntimeError(f"{status=} is unknown")
            if status == "invoices__paid":
                #  TODO Save New Invoice
                await self._paid_invoice_and_save_to_db(message)

        except RuntimeError as why:
            logger.error(f"{why}")

        except ConnectionError as why:
            logger.critical(f"{why}")

        except BaseException as why:
            logger.critical(f"Failed processing response {status=} => {why}")
