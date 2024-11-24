from rich import print
from typer import Typer

from .pdf import PDF, PdfMetaData

pdf = Typer(name="pdf")


@pdf.command()
def get_metadata(path: str):
    pdf = PDF(path)

    metadata = pdf.get_metadata()

    if metadata:
        print(metadata)


@pdf.command()
def set_metadata(path: str, title: str, author: str, subject: str) -> None:
    pdf = PDF(path)
    pdf.set_metadata(PdfMetaData(title=title, author=author, subject=subject))
