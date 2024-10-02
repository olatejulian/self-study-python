import logging

from .ltx_config import LtxConfig
from .ltx_service import LtxService
from .ltxrc import LtxrcJsonLoader
from .utils import ProcessRunner


def LtxServiceFactory() -> LtxService:
    ltxrc_parser = LtxrcJsonLoader()

    ltxrc = ltxrc_parser.load()

    ltx_config = LtxConfig(
        dirs=ltxrc["dirs"],
        args=ltxrc["args"],
    )

    logger = logging.Logger(__name__)

    process_runner = ProcessRunner(logger=logger)

    ltx_service = LtxService(
        config=ltx_config,
        process_runner=process_runner,
    )

    return ltx_service
