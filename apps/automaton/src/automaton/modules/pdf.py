from pypdf import DocumentInformation, PdfReader, PdfWriter


def is_pdf_file(file_path: str) -> bool:
    return file_path.endswith(".pdf")


class PdfMetaData:
    def __init__(
        self,
        title: str | None = None,
        author: str | None = None,
        creator: str | None = None,
        subject: str | None = None,
        keywords: str | None = None,
        producer: str | None = None,
        creation_date: str | None = None,
        modification_date: str | None = None,
        **kwargs,
    ):
        self.title = title
        self.author = author
        self.creator = creator
        self.subject = subject
        self.keywords = keywords
        self.producer = producer
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.custom_fields = kwargs

    def to_dict(self) -> dict[str, str]:
        template = {
            "/Title": self.title,
            "/Author": self.author,
            "/Creator": self.creator,
            "/Producer": self.producer,
            "/Subject": self.subject,
            "/Keywords": self.keywords,
            "/ModDate": self.modification_date,
            "/CreationDate": self.creation_date,
        }

        return {key: value for key, value in template.items() if value}


class PDF:
    def __init__(self, file_path: str):
        self.__reader = PdfReader(file_path)
        self.__writer = PdfWriter(self.__reader)
        self.__file_path = file_path

    def get_metadata(self) -> DocumentInformation | None:
        return self.__reader.metadata

    def set_metadata(self, metadata: PdfMetaData) -> None:
        self.__writer.add_metadata(infos=metadata.to_dict())

        with open(self.__file_path, "wb") as file:
            self.__writer.write(file)
