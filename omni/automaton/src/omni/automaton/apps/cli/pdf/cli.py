from typer import Typer

from .. import common
from . import commands

pdf_cli = Typer(name="pdf")


@pdf_cli.command()
def set_metadata(
    pdf_path: str,
    title: str | None = None,
    author: str | None = None,
    creator: str | None = None,
    subject: str | None = None,
    keywords: str | None = None,
    producer: str | None = None,
    creation_date: str | None = None,
    modification_date: str | None = None,
):
    common.try_run(
        commands.set_metadata,
        pdf_path=pdf_path,
        title=title,
        author=author,
        creator=creator,
        subject=subject,
        keywords=keywords,
        producer=producer,
        creation_date=creation_date,
        modification_date=modification_date,
    )


@pdf_cli.command()
def get_metadata(pdf_path: str):
    common.try_run(
        commands.get_metadata,
        pdf_path=pdf_path,
    )


@pdf_cli.command()
def title_as_file_name(pdf_path: str):
    common.try_run(commands.set_title_as_file_name, pdf_path=pdf_path)


@pdf_cli.command()
def set_many_title_as_file_name(dir_path: str):
    common.try_run(commands.set_many_title_as_file_name, directory_path=dir_path)
