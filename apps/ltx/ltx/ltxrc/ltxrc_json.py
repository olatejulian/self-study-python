from pathlib import Path

from pydantic import TypeAdapter

from ..utils import PathResolveAbsolute
from .__exceptions__ import LtxrcSchemaException
from .__types__ import LtxrcDict
from .ltxrc_abc import Ltxrc


class LtxrcJsonLoader(Ltxrc):
    def load(self) -> LtxrcDict:
        path = Path(".")

        LTXRC_FILE_NAME = ".ltxrc.json"

        ltxrc_file = PathResolveAbsolute(path / LTXRC_FILE_NAME)

        if not ltxrc_file.exists() or not ltxrc_file.is_file():
            raise FileNotFoundError

        ltxrc_bytes = ltxrc_file.read_bytes()

        try:
            ltxrc_schema_validation = TypeAdapter(LtxrcDict)

            ltxrc = ltxrc_schema_validation.validate_json(ltxrc_bytes)

        except Exception as exc:
            raise LtxrcSchemaException(exc) from exc

        else:
            print(ltxrc)

            return ltxrc
