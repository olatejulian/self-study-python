import logging
import subprocess


class ProcessRunner:
    def __init__(self, logger: logging.Logger | None = None):
        self.__logger = logger or logging.getLogger(__name__)

    def run(self, command: list[str]) -> None:
        command_str = "\n    ".join(command)

        try:
            msg = "Exec:\n" + command_str

            self.__logger.info(msg)

            output = subprocess.run(command, capture_output=True, text=True)

        except subprocess.CalledProcessError as subprocess_error:
            self.__logger.exception(subprocess_error.returncode)

            self.__logger.error(subprocess_error.stderr)

        else:
            self.__logger.info(output.stdout)

        finally:
            self.__logger.info("Finished executing: " + command_str)
