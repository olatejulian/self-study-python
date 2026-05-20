from pathlib import Path


class GitIgnorePatterns:
    def __init__(
        self,
        root: Path,
        *extended_patterns: str,
    ) -> None:
        self.__root = root.resolve()
        self.__extended_patterns = list(extended_patterns)

    def load(self) -> list[str]:
        gitignore_path = self.__root / ".gitignore"

        patterns: list[str] = []

        if gitignore_path.is_file():
            with gitignore_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                patterns.extend(
                    line.strip()
                    for line in file
                    if line.strip() and not line.lstrip().startswith("#")
                )

        patterns.extend(self.__extended_patterns)

        return patterns
