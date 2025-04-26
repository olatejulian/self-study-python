from typing import Optional

from typer import Typer

from .. import common
from . import commands

pdf_cli = Typer(name="pdf")


@pdf_cli.command()
def set_metadata(
    pdf_path: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    creator: Optional[str] = None,
    subject: Optional[str] = None,
    keywords: Optional[str] = None,
    producer: Optional[str] = None,
    creation_date: Optional[str] = None,
    modification_date: Optional[str] = None,
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
    common.try_run(
        commands.set_many_title_as_file_name, directory_path=dir_path
    )
