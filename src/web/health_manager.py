# BUILTIN modules
from typing import List

# Third party modules
from loguru import logger

# local modules
from ..repository.data_adapter import DataOperationsRepository
from ..tools.rabbit_client import AbstractRobustConnection
from .api.schemas import HealthSchema, ResourceSchema


class HealthManager:
    """This class handles health status reporting on used resources."""

    # ---------------------------------------------------------
    #
    def __init__(
        self, connection: AbstractRobustConnection, repository: DataOperationsRepository
    ):
        """Class initializer.

        :param repository: Data layer handler object.
        :param connection: 'RabbitMQ' connection object.
        """
        self.repo = repository
        self.connection = connection

    async def _get_rabbit_status(self) -> List[ResourceSchema]:
        """Return RabbitMQ connection status.

        :return: RabbitMQ connection status.
        """

        try:
            status = not self.connection.is_closed
        except BaseException as why:
            logger.critical(f"RabbitMQ: {why}")
            status = False

        return [ResourceSchema(name="RabbitMQ", status=status)]

    async def get_status(self) -> HealthSchema:
        """Return Health status for used resources.

        :return: Service health status.
        """
        resource_items = []
        resource_items += await self._get_rabbit_status()
        total_status = all(key.status for key in resource_items)

        return HealthSchema(
            status=total_status,
            # version=self.version,
            # name=self.service_name,
            resources=resource_items,
        )
