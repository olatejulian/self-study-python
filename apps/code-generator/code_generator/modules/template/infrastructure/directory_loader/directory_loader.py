from pathlib import Path

from code_generator.modules.template import Directory, DirectoryLoader, File


class FSDirectoryLoader(DirectoryLoader):
    @classmethod
    def load(cls, dir_path: str) -> Directory:
        path = Path(dir_path).resolve().absolute()

        if not path.exists():
            raise FileNotFoundError

        return Directory(
            name=path.name,
            contents=[
                cls.__load_sub_content(sub_content)
                for sub_content in path.iterdir()
            ],
        )

    @staticmethod
    def __load_file(file_path: Path) -> File:
        file_name = file_path.name + file_path.suffix

        file_content = file_path.read_text().encode()

        return File(name=file_name, content=file_content)

    @classmethod
    def __load_directory(cls, directory_path: Path) -> Directory:
        directory_name = directory_path.name

        directory_contents = [
            cls.__load_sub_content(sub_content)
            for sub_content in directory_path.iterdir()
        ]

        return Directory(name=directory_name, contents=directory_contents)

    @classmethod
    def __load_sub_content(cls, path: Path) -> File | Directory:
        return (
            cls.__load_file(path)
            if path.is_file()
            else cls.__load_directory(path)
        )
