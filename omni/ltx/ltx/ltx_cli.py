import rich
from typer import Typer

from .ltx_container import GetLtxService
from .ltxrc import JsonLtxrcParser

ltx_cli = Typer(name="ltx")


@ltx_cli.command()
def build(
    file_name: str,
):
    ltx_service = GetLtxService()

    ltx_service.post_init()

    ltx_service.latexmk(file_name)


@ltx_cli.command()
def config(absolute: bool = False):
    ltxrc_parser = JsonLtxrcParser()

    ltx_config = ltxrc_parser.get_configuration()

    rich.print(
        "Latexmk Arguments:",
        *["  " + argument for argument in ltx_config["arguments"]],
        sep="\n",
        end="\n\n",
    )

    if absolute:
        directories_title = "Directories (Absolute Paths):"

    else:
        directories_title = "Directories (Root Relative Paths):"

    rich.print(
        directories_title,
        *[
            f"  {dir_type.capitalize()}: {dir_name}"
            for dir_type, dir_name in ltx_config["directories"].items()
        ],
        sep="\n",
    )
