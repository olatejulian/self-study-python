from pathlib import Path


def Latexmk(file_path: Path, args: list[str] | None = None) -> list[str]:
    __args: list[str] = sorted(args, key=lambda x: x.lower()) if args else []

    cmd = ["latexmk", *__args, str(file_path.resolve().absolute())]

    print(cmd)

    return cmd
