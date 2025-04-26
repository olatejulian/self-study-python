from .ltx_config import LtxConfig
from .utils import Latexmk, ProcessRunner, Texinputs


class LtxService:
    def __init__(
        self,
        config: LtxConfig,
        process_runner: ProcessRunner,
    ):
        self.__config = config
        self.__process_runner = process_runner

    def post_init(self):
        self.__config.create_directories()

        dirs = self.__config.paths

        texinputs = Texinputs(paths=[dirs["source"], dirs["resources"]])

        texinputs.export()

    def latexmk(self, file_name: str) -> None:
        source_path = self.__config.paths["source"]

        file_path = source_path / file_name

        latexmk_default_args = [
            f"-auxdir={self.__config.paths["build"]}",
            f"-outdir={self.__config.paths["output"]}",
        ]

        latexmk_config_args = self.__config.args

        latexmk_args = latexmk_default_args + latexmk_config_args

        latexmk = Latexmk(file_path, latexmk_args)

        self.__process_runner.run(latexmk)
