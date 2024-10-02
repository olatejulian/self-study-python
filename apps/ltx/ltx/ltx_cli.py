from typer import Typer

from .ltx_service_factory import LtxServiceFactory


def cli() -> Typer:
    __cli = Typer(name="ltx")

    service = LtxServiceFactory()

    def build(file_name: str) -> None:
        service.post_init()

        service.latexmk(file_name)

    __cli.command("build")(build)

    return __cli()
