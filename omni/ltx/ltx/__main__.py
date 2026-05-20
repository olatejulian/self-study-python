from ltx.ltx_cli import ltx_cli
from ltx.ltx_container import LtxContainer


def main():
    ltx_container = LtxContainer()

    ltx_container.wire(modules=[__name__])

    return ltx_cli()


main()
