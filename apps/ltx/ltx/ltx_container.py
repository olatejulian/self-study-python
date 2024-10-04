import logging

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Resource, Singleton
from dependency_injector.wiring import Provide, inject

from .ltx_service import LtxService
from .ltxrc import LtxrcJsonLoader
from .utils.process_runner import ProcessRunner


class LtxContainer(DeclarativeContainer):
    ltx_config = Resource(lambda: LtxrcJsonLoader().load())

    logger = logging.getLogger(__name__)

    process_runner = Singleton(ProcessRunner, logger=logger)

    ltx_service = Singleton(
        LtxService,
        config=ltx_config,
        process_runner=process_runner,
    )


@inject
def GetLtxService(
    ltx_service: LtxService = Provide[LtxContainer.ltx_service],
):
    return ltx_service
