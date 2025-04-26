
import rich

from automaton.modules import path as p
from automaton.modules import pdf


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
    pdf.PDF(pdf_path).set_metadata(
        pdf.PdfMetaData(
            title,
            author,
            creator,
            subject,
            keywords,
            producer,
            creation_date,
            modification_date,
        )
    )


def get_metadata(pdf_path: str):
    if pdf_metadata := pdf.PDF(pdf_path).get_metadata():
        metadata_dict = {
            "title": pdf_metadata.title,
            "author": pdf_metadata.author,
            "subject": pdf_metadata.subject,
            "creation-date": pdf_metadata.creation_date,
            "modification-date": pdf_metadata.modification_date,
            "producer": pdf_metadata.producer,
            "creator": pdf_metadata.creator,
        }

        rich.print(metadata_dict)


def set_title_as_file_name(pdf_path: str):
    file_name = p.get_file_name(pdf_path)

    pdf.PDF(pdf_path).set_metadata(pdf.PdfMetaData(title=file_name))


def set_many_title_as_file_name(directory_path: str):
    path = p.verify_path(directory_path)

    for file in p.list_files(path):
        if pdf.is_pdf_file(file):
            pdf.PDF(path).set_metadata(
                pdf.PdfMetaData(title=p.get_file_name(file))
            )
