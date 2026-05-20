import sys

from omni.pyls.src.omni.pyls.app.cli import typer_cli


def main():
    typer_cli()

    return 0


if __name__ == "__main__":
    sys.exit(main())
