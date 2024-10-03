from rich.console import Console
from typer import Typer

from .__exceptions__ import (
    LtxConfigCannotMakeDirectoryException,
    LtxConfigDidNotMakeDirectoriesException,
)
from .ltx_service_factory import LtxServiceFactory
from .ltxrc import LtxrcSchemaException


def cli() -> Typer:
    __cli = Typer(name="ltx")

    console = Console(stderr=True)

    service = LtxServiceFactory()

    def build(file_name: str) -> None:
        try:
            service.post_init()

        except LtxConfigCannotMakeDirectoryException as e:
            console.print(e)

        except LtxConfigDidNotMakeDirectoriesException as e:
            console.print(e)

        except LtxrcSchemaException as e:
            console.print(e)

        else:
            service.latexmk(file_name)

        finally:
            __cli.command("build")(build)

    return __cli()
