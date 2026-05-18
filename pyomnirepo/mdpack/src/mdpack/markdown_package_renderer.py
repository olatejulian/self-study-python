from pathlib import Path


class MarkdownPackageRenderer:
    def __init__(
        self,
        root: Path,
        tree: str,
        contents: str,
    ) -> None:
        self.__root = root
        self.__tree = tree
        self.__contents = contents

    def render(
        self,
    ) -> str:
        return (
            f"# {self.__root.name}\n\n"
            f"## Project Structure\n\n"
            f"```\n{self.__tree}\n```\n\n"
            f"## File Contents\n\n"
            f"{self.__contents}\n"
        )
