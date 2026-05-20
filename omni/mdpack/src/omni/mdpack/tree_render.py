from pathlib import Path

from .traversal import TraversalEvent, TraversalEventType


class TreeRenderer:
    """
    Render a directory tree similar to Unix `tree`.
    """

    __TEE = "├── "
    __ELBOW = "└── "
    __PIPE = "│   "

    def __init__(self) -> None:
        self.__lines: list[str] = []

        self.__branch_stack: list[bool] = []

    def consume(
        self,
        event: TraversalEvent,
    ) -> None:
        if event.type == TraversalEventType.EXIT_DIRECTORY:
            if self.__branch_stack:
                self.__branch_stack.pop()

            return

        if event.depth == 0:
            self.__lines.append(event.path.name)

            self.__branch_stack.append(not event.is_last)

            return

        prefix = ""

        for has_more in self.__branch_stack[:-1]:
            prefix += self.__PIPE if has_more else self.__PIPE

        connector = self.__ELBOW if event.is_last else self.__TEE

        self.__lines.append(f"{prefix}{connector}{event.path.name}")

        if event.type == TraversalEventType.ENTER_DIRECTORY:
            self.__branch_stack.append(not event.is_last)

    def render(
        self,
    ) -> str:
        return "\n".join(self.__lines)


class MarkdownRenderer:
    """
    Render markdown file sections from traversal events.
    """

    __MAX_BINARY_CHECK_SIZE = 1024
    __MAX_TEXT_FILE_SIZE = 1_000_000

    def __init__(
        self,
        root: Path,
    ) -> None:
        self.__root = root.resolve()

        self.__sections: list[str] = []

    def consume(
        self,
        event: TraversalEvent,
    ) -> None:
        if event.type != TraversalEventType.FILE:
            return

        path = event.path

        if self.__is_binary(path):
            return

        try:
            content = path.read_text(
                encoding="utf-8",
            )

        except (
            OSError,
            UnicodeDecodeError,
        ):
            return

        relative = path.relative_to(self.__root)

        language = self.__language(path)

        fence = self.__fence(content)

        section = f"### {relative.as_posix()}\n\n{fence}{language}\n{content}\n{fence}"

        self.__sections.append(section)

    def render(
        self,
    ) -> str:
        return "\n\n".join(self.__sections)

    def __language(
        self,
        path: Path,
    ) -> str:
        suffixes = [suffix.removeprefix(".") for suffix in path.suffixes]

        language = "".join(suffixes)

        return language or "text"

    def __fence(
        self,
        content: str,
    ) -> str:
        fence = "```"

        while fence in content:
            fence += "`"

        return fence

    def __is_binary(
        self,
        path: Path,
    ) -> bool:
        try:
            if path.stat().st_size > self.__MAX_TEXT_FILE_SIZE:
                return True

            with path.open("rb") as file:
                chunk = file.read(self.__MAX_BINARY_CHECK_SIZE)

        except OSError:
            return True

        return b"\0" in chunk
