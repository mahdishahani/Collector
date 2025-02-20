# Third party modules
from fastapi import Depends
from loguru import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.repository.db import async_engine, get_async_session

# Local modules


class DataOperationsRepository:
    @staticmethod
    async def _write(model_instance):
        try:
            async with AsyncSession(async_engine) as db:
                # Add the model_instance to the session
                db.add(model_instance)
                # Commit the changes to the database
                await db.commit()
                await db.refresh(model_instance)
                return model_instance
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy errors
            logger.critical(f"SQLAlchemy Error: {sql_err}")
            await db.rollback()

        except IntegrityError as integrity_err:
            # Handle integrity constraint violations
            logger.critical(f"Integrity Error: {integrity_err}")
            await db.rollback()
        except Exception as e:
            # Handle other exceptions
            logger.critical(f"Failed processing response => {e}")
            await db.rollback()

    async def _read(self, db: AsyncSession = Depends(get_async_session)):
        pass
