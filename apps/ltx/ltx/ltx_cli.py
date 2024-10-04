from typer import Typer

from .ltx_container import GetLtxService

ltx_cli = Typer(name="ltx")


@ltx_cli.command()
def ltx(
    file_name: str,
):
    ltx_service = GetLtxService()

    ltx_service.post_init()

    ltx_service.latexmk(file_name)
