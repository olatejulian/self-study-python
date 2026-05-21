from pathlib import Path

import typer
from omni.mdpack.src.omni.mdpack.ignore import GitIgnorePatterns
from omni.mdpack.src.omni.mdpack.markdown_package_builder import MarkdownPackageBuilder


def cli(
    root_directory: Path = typer.Argument(
        default=Path.cwd(),
        help="Path to directory to pack.",
    ),
    ignore_patterns: list[str] = typer.Option(
        "--ignore", "-i", help="Ignore patterns (glob syntax)."
    ),
) -> None:
    root = root_directory.resolve()

    output_path = root / f"{root.name}.md"

    ignore_patterns = GitIgnorePatterns(
        root,
        f"**/{output_path.name}",
        *ignore_patterns,
    ).load()

    markdown = MarkdownPackageBuilder(
        root,
        ignore_patterns,
    ).build()

    output_path.write_text(
        markdown,
        encoding="utf-8",
    )

    typer.echo(f"Directory packed into {output_path.as_posix()}")


def main() -> None:
    typer.run(cli)


if __name__ == "__main__":
    main()
