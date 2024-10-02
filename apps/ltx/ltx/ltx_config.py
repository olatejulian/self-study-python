from pathlib import Path

from .__exceptions__ import (
    LtxConfigCannotMakeDirectoryException,
    LtxConfigDidNotMakeDirectoriesException,
)
from .__types__ import (
    LtxConfigDirPathsDict,
    LtxConfigDirsDict,
)
from .utils import PathResolveAbsolute


class LtxConfig:
    __paths: LtxConfigDirPathsDict

    def __init__(
        self,
        dirs: LtxConfigDirsDict,
        args: list[str],
    ):
        self.__dirs = dirs
        self.__args = args

    @property
    def paths(self) -> LtxConfigDirPathsDict:
        if not self.__paths:
            raise LtxConfigDidNotMakeDirectoriesException

        return self.__paths

    @property
    def args(self) -> list[str]:
        return self.__args

    def create_directories(self) -> None:
        root = Path(self.__dirs["root"])

        build = root / self.__dirs["build"]

        output = root / self.__dirs["output"]

        resources = root / self.__dirs["resources"]

        source = root / self.__dirs["source"]

        path_dict = {
            "root": root,
            "build": build,
            "output": output,
            "resources": resources,
            "source": source,
        }

        try:
            for key, path in path_dict.items():
                absolute_path = PathResolveAbsolute(path)

                absolute_path.mkdir(parents=True, exist_ok=True)

                assert absolute_path.exists()

                path_dict[key] = absolute_path

        except Exception as exc:
            raise LtxConfigCannotMakeDirectoryException(exc) from exc

        else:
            self.__paths = LtxConfigDirPathsDict(**path_dict)
