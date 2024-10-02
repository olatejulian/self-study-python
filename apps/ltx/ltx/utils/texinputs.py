import os
from pathlib import Path


class Texinputs:
    def __init__(self, paths: list[Path]):
        self.__paths = paths

    def export(self) -> None:
        sep = os.pathsep

        TEXINPUTS = "TEXINPUTS"

        paths = [str(path.resolve().absolute()) for path in self.__paths]

        for path in paths:
            texinputs = os.getenv(TEXINPUTS, "")

            if not texinputs:
                os.environ[TEXINPUTS] = path

            os.environ[TEXINPUTS] = path + sep + texinputs
