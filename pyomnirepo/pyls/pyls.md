# PYLS

## Project Structure

```
pyls
├──  README.md
├──  pyls
│   ├──  __init__.py
│   ├──  __main__.py
│   ├──  __pycache__
│   │   ├──  __init__.cpython-312.pyc
│   │   ├──  __main__.cpython-312.pyc
│   │   ├──  cli.cpython-312.pyc
│   │   ├──  filtering.cpython-312.pyc
│   │   ├──  provider.cpython-312.pyc
│   │   ├──  rendering.cpython-312.pyc
│   │   ├──  repository.cpython-312.pyc
│   │   ├──  service.cpython-312.pyc
│   │   ├──  sorting.cpython-312.pyc
│   │   └──  traversal.cpython-312.pyc
│   ├──  app
│   │   ├──  __init__.py
│   │   └──  cli.py
│   ├──  filtering
│   │   ├──  __init__.py
│   │   ├──  abc_filtering.py
│   │   ├──  di_filtering.py
│   │   └──  impl_filtering.py
│   ├──  provider
│   │   ├──  __init__.py
│   │   └──  children.py
│   ├──  rendering
│   │   ├──  __init__.py
│   │   ├──  abc_rendering.py
│   │   ├──  di_rendering.py
│   │   └──  impl_rendering.py
│   ├──  sorting
│   │   ├──  __init__.py
│   │   ├──  __pycache__
│   │   │   ├──  __init__.cpython-312.pyc
│   │   │   └──  traversal.cpython-312.pyc
│   │   ├──  abc_sorting.py
│   │   ├──  di_sorting.py
│   │   └──  impl_sorting.py
│   └──  traversal
│       ├──  __init__.py
│       ├──  abc_traversal.py
│       ├──  di_traversal.py
│       └──  impl_traversal.py
└──  pyproject.toml
```

## File Contents

### README.md

```md
# PyLS - List Directory Contents

```

### pyls/__init__.py

```py

```

### pyls/__main__.py

```py
import sys

from pyls.app.cli import typer_cli


def main():
    typer_cli()

    return 0


if __name__ == "__main__":
    sys.exit(main())

```

### pyls/app/__init__.py

```py

```

### pyls/app/cli.py

```py
from pathlib import Path

from pyls.filtering.di_filtering import FilterToken, get_filter
from pyls.sorting.di_sorting import SortToken, get_sorter
from pyls.traversal.di_traversal import TraversalToken, get_traversal
from pyls.rendering.di_rendering import RendererToken, get_renderer

from typer import Argument, Option, Typer

typer_cli = Typer(name="pyls")


@typer_cli.command()
def pyls(
    path: Path = Argument(
        Path("."),
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=False,
    ),
    sort_by: SortToken = Option(SortToken.NAME, "--sort-by", "-s"),
    ascending: bool = Option(True, "--ascending/--descending"),
    first: bool = Option(True, "--dirs-first/--files-first"),
    hidden: bool = Option(True, "--hidden/--no-hidden"),
    ignore: list[str] = Option([], "--ignore", "-i"),
    gitignore: bool = Option(True, "--gitignore", "-g"),
    depth: int = Option(-1, "--depth", "-d"),
    method: str = Option("breadth-first", "--method", "-m"),
    output: str = Option("rich", "--output", "-o"),
) -> None:



```

### pyls/filtering/__init__.py

```py
from .di_filtering import FILTER_STRATEGIES, FilterToken

__all__ = ["FILTER_STRATEGIES", "FilterToken"]

```

### pyls/filtering/abc_filtering.py

```py
from pathlib import Path
from typing import Protocol


class FilterStrategy(Protocol):
    def apply(self, path: Path) -> bool: ...

```

### pyls/filtering/di_filtering.py

```py
from enum import StrEnum
from typing import Callable

from .abc_filtering import FilterStrategy
from .impl_filtering import (
    CompositeFilter,
    GitIgnoreFilter,
    HiddenFilter,
    NoFilter,
    PatternFilter,
)


class FilterToken(StrEnum):
    NO = "filter.no"
    HIDDEN = "filter.hidden"
    GITIGNORE = "filter.gitignore"
    PATTERN = "filter.pattern"
    COMPOSITE = "filter.composite"


di: dict[FilterToken, Callable[..., FilterStrategy]] = {
    FilterToken.NO: lambda: NoFilter(),
    FilterToken.HIDDEN: lambda: HiddenFilter(),
    FilterToken.GITIGNORE: lambda root: GitIgnoreFilter(root),
    FilterToken.PATTERN: lambda patterns: PatternFilter(patterns),
    FilterToken.COMPOSITE: lambda *filters: CompositeFilter(*filters),
}


def get_filter(token: FilterToken, *args, **kwargs) -> FilterStrategy:
    return di[token](*args, **kwargs)

```

### pyls/filtering/impl_filtering.py

```py
from pathlib import Path

from pathspec import PathSpec

from .abc_filtering import FilterStrategy


class NoFilter(FilterStrategy):
    def apply(self, path: Path) -> bool:
        _ = path

        return True


class HiddenFilter(FilterStrategy):
    def apply(self, path: Path) -> bool:
        return not path.name.startswith(".")


class PatternFilter(FilterStrategy):
    def __init__(self, patterns: list[str]) -> None:
        self.__spec = PathSpec.from_lines("gitwildmatch", patterns)

    def apply(self, path: Path) -> bool:
        return not self.__spec.match_file(str(path))


class GitIgnoreFilter(FilterStrategy):
    def __init__(self, root: Path) -> None:
        self.__root = root.resolve()

        gitignore = self.__root / ".gitignore"
        if gitignore.exists():
            lines = gitignore.read_text().splitlines()
        else:
            lines = []

        self.__spec = PathSpec.from_lines("gitwildmatch", lines)

    def apply(self, path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(self.__root)
        except ValueError:
            return True  # outside root

        return not self.__spec.match_file(str(relative))


class CompositeFilter(FilterStrategy):
    def __init__(self, *filters: FilterStrategy) -> None:
        self.__filters = filters

    def apply(self, path: Path) -> bool:
        return all(f.apply(path) for f in self.__filters)

```

### pyls/provider/__init__.py

```py

```

### pyls/provider/children.py

```py
from pathlib import Path
from typing import Iterable, Iterator

from pyls.filtering.abc_filtering import FilterStrategy
from pyls.sorting.abc_sorting import SortStrategy


class ChildrenCallbackProvider:
    def __init__(self, filterer: FilterStrategy, sorter: SortStrategy):
        self.__filterer = filterer
        self.__sorter = sorter

    def __call__(self, path: Path) -> Iterable[Path]:
        return self.__iter_children(path)

    def __iter_children(self, path: Path) -> Iterator[Path]:
        entries = path.iterdir()

        filtered_entries = (entry for entry in entries if self.__filterer.apply(entry))

        sorted_entries = sorted(filtered_entries, key=self.__sorter.key)

        for entry in sorted_entries:
            yield entry

```

### pyls/rendering/__init__.py

```py

```

### pyls/rendering/abc_rendering.py

```py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Renderer(ABC, Generic[Input, Output]):
    @abstractmethod
    def render(self, input: Input) -> Output: ...

```

### pyls/rendering/di_rendering.py

```py
from enum import StrEnum
from typing import Callable

from .abc_rendering import Renderer
from .impl_rendering import RichTreeRenderer


class RendererToken(StrEnum):
    RICH = "rich"


di: dict[RendererToken, Callable[..., Renderer]] = {
    RendererToken.RICH: lambda clear_console: RichTreeRenderer(clear_console),
}


def get_renderer(token: RendererToken, *args, **kwargs) -> Renderer:
    return di[token](*args, **kwargs)

```

### pyls/rendering/impl_rendering.py

```py
from pathlib import Path
from typing import Optional, Union

from rich.console import Console
from rich.tree import Tree

from pyls.traversal.impl_traversal import (
    BreadthTraversalEvent,
    BreadthTraversalState,
    DepthTraversalEvent,
    DepthTraversalState,
)

# We unify event interface for simplicity:
TraversalEvent = Union[DepthTraversalEvent, BreadthTraversalEvent]


class RichTreeRenderer:
    """
    Renderer that produces a visual tree using rich.
    Expects traversal events in a sequence of:
        ENTER_DIR, FILE, EXIT_DIR.
    """

    def __init__(self, *, clear_console: bool = False) -> None:
        self.console = Console()
        self._stack: list[Tree] = []
        self._root_tree: Optional[Tree] = None
        self._clear = clear_console

    def render(self, event: TraversalEvent) -> None:
        """
        Render a single event.
        """
        # Dispatch based on event.state
        state = event.state

        # Directory entered
        if (
            state is DepthTraversalState.ENTER_DIR
            or state is BreadthTraversalState.ENTER_DIR
        ):
            self._enter_dir(event.path, event.depth)

        # File
        elif state is DepthTraversalState.FILE or state is BreadthTraversalState.FILE:
            self._file(event.path, event.depth)

        # Directory exit
        elif (
            state is DepthTraversalState.EXIT_DIR
            or state is BreadthTraversalState.EXIT_DIR
        ):
            self._exit_dir()

    def _enter_dir(self, path: Path, depth: int) -> None:
        """
        Called when a directory is entered.
        """
        # Label with directory icon and name
        label = f"📁 {path.name}"

        if depth == 0:
            # Root directory, create root tree
            self._root_tree = Tree(label)
            self._stack.append(self._root_tree)
        else:
            parent = self._stack[-1]
            branch = parent.add(label)
            self._stack.append(branch)

    def _file(self, path: Path, depth: int) -> None:
        """
        Called for file events.
        """
        label = f"📄 {path.name}"

        if not self._stack:
            # If no current stack, we just print directly
            self.console.print(label)
        else:
            parent = self._stack[-1]
            parent.add(label)

    def _exit_dir(self) -> None:
        """
        Pop current directory branch.
        """
        if len(self._stack) > 1:
            self._stack.pop()

    def finalize(self) -> None:
        """
        Must be called after traversal to print the tree to console.
        """
        if self._root_tree is not None:
            if self._clear:
                self.console.clear()
            self.console.print(self._root_tree)

```

### pyls/sorting/__init__.py

```py

```

### pyls/sorting/abc_sorting.py

```py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

KeyType = TypeVar("KeyType")


class SortStrategy(ABC, Generic[KeyType]):
    @abstractmethod
    def key(self, path: Path) -> KeyType: ...

```

### pyls/sorting/di_sorting.py

```py
from enum import StrEnum
from typing import Callable

from .abc_sorting import SortStrategy
from .impl_sorting import (
    CreatedTimeStrategy,
    ExtensionStrategy,
    ModifiedTimeStrategy,
    NameStrategy,
)


class SortToken(StrEnum):
    NAME = "name"
    EXTENSION = "extension"
    CREATED_TIME = "created_time"
    MODIFIED_TIME = "modified_time"


di: dict[SortToken, Callable[..., SortStrategy]] = {
    SortToken.NAME: lambda: NameStrategy(),
    SortToken.EXTENSION: lambda: ExtensionStrategy(),
    SortToken.CREATED_TIME: lambda: CreatedTimeStrategy(),
    SortToken.MODIFIED_TIME: lambda: ModifiedTimeStrategy(),
}


def get_sorter(token: SortToken, *args, **kwargs) -> SortStrategy:
    return di[token](*args, **kwargs)

```

### pyls/sorting/impl_sorting.py

```py
from pathlib import Path

from .abc_sorting import SortStrategy


class NameStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return path.name.casefold()


class ExtensionStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return path.suffix.casefold()


class CreatedTimeStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return str(path.stat().st_ctime)


class ModifiedTimeStrategy(SortStrategy):
    def key(self, path: Path) -> str:
        return str(path.stat().st_mtime)

```

### pyls/traversal/__init__.py

```py

```

### pyls/traversal/abc_traversal.py

```py
from abc import ABC, abstractmethod
from typing import Generic, Iterator, Self, TypeVar

T = TypeVar("T")


class TraversalStrategy(ABC, Generic[T], Iterator[T]):
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError

```

### pyls/traversal/di_traversal.py

```py
from enum import StrEnum
from typing import Callable

from pyls.traversal.abc_traversal import TraversalStrategy
from pyls.traversal.impl_traversal import BreadthFirstStrategy, DepthFirstStrategy


class TraversalToken(StrEnum):
    DFS = "dfs"
    BFS = "bfs"


di: dict[TraversalToken, Callable[..., TraversalStrategy]] = {
    TraversalToken.DFS: lambda root, callback, max_depth: DepthFirstStrategy(
        root, callback, max_depth
    ),
    TraversalToken.BFS: lambda root, callback, max_depth: BreadthFirstStrategy(
        root, callback, max_depth
    ),
}


def get_traversal(token: TraversalToken, *args, **kwargs) -> TraversalStrategy:
    return di[token](*args, **kwargs)

```

### pyls/traversal/impl_traversal.py

```py
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Deque, Iterable, Iterator, Optional

from pyls.traversal.abc_traversal import TraversalStrategy

Callback = Callable[[Path], Iterable[Path]]


class DepthTraversalState(Enum):
    ENTER_DIR = auto()
    EXIT_DIR = auto()
    FILE = auto()


@dataclass(frozen=True)
class DepthTraversalEvent:
    path: Path
    state: DepthTraversalState
    depth: int


class DepthFirstStrategy(TraversalStrategy[DepthTraversalEvent]):
    def __init__(
        self,
        root: Path,
        callback: Callback,
        max_depth: int,
    ) -> None:
        self._stack: list[
            tuple[Path, Optional[Iterator[Path]], int, DepthTraversalState]
        ] = [(root, None, 0, DepthTraversalState.ENTER_DIR)]
        self._callback = callback
        self._max_depth = max_depth

    def __iter__(self):
        return self

    def __next__(self) -> DepthTraversalEvent:
        while self._stack:
            node, children_iter, depth, state = self._stack.pop()

            # ENTER_DIR
            if state is DepthTraversalState.ENTER_DIR:
                # schedule exit
                self._stack.append((node, None, depth, DepthTraversalState.EXIT_DIR))

                # schedule children iterator
                if self._max_depth < 0 or depth < self._max_depth:
                    children_iter = iter(self._callback(node))
                    self._stack.append(
                        (node, children_iter, depth, DepthTraversalState.FILE)
                    )
                return DepthTraversalEvent(node, DepthTraversalState.ENTER_DIR, depth)

            # CHILDREN iterator handler
            if children_iter is not None:
                try:
                    child = next(children_iter)
                except StopIteration:
                    continue

                # push back same iterator
                self._stack.append(
                    (node, children_iter, depth, DepthTraversalState.FILE)
                )

                # now schedule child
                if child.is_dir():
                    self._stack.append(
                        (child, None, depth + 1, DepthTraversalState.ENTER_DIR)
                    )
                else:
                    return DepthTraversalEvent(
                        child, DepthTraversalState.FILE, depth + 1
                    )
                continue

            # EXIT_DIR
            if state is DepthTraversalState.EXIT_DIR:
                return DepthTraversalEvent(node, DepthTraversalState.EXIT_DIR, depth)

        raise StopIteration


class BreadthTraversalState(Enum):
    ENTER_DIR = auto()
    EXIT_DIR = auto()
    FILE = auto()


@dataclass(frozen=True)
class BreadthTraversalEvent:
    path: Path
    state: BreadthTraversalState
    depth: int


class BreadthFirstStrategy(TraversalStrategy[BreadthTraversalEvent]):
    def __init__(self, root: Path, callback: Callback, max_depth: int) -> None:
        self._queue: Deque[tuple[Path, int]] = deque([(root, 0)])
        self._callback = callback
        self._max_depth = max_depth

        self._pending_files: Deque[BreadthTraversalEvent] = deque()
        self._pending_exit: BreadthTraversalEvent | None = None

    def __iter__(self):
        return self

    def __next__(self) -> BreadthTraversalEvent:
        if self._pending_files:
            return self._pending_files.popleft()

        if self._pending_exit:
            ev = self._pending_exit
            self._pending_exit = None
            return ev

        if not self._queue:
            raise StopIteration

        node, depth = self._queue.popleft()

        # Schedule EXIT
        self._pending_exit = BreadthTraversalEvent(
            node, BreadthTraversalState.EXIT_DIR, depth
        )

        # Collect children
        if self._max_depth < 0 or depth < self._max_depth:
            for child in self._callback(node):
                if child.is_dir():
                    self._queue.append((child, depth + 1))
                else:
                    self._pending_files.append(
                        BreadthTraversalEvent(
                            child, BreadthTraversalState.FILE, depth + 1
                        )
                    )

        return BreadthTraversalEvent(node, BreadthTraversalState.ENTER_DIR, depth)

```

### pyproject.toml

```toml
[build-system]
build-backend = "pdm.backend"
requires = ["pdm-backend"]

[project]
authors = [{email = "julian.lf.olate@gmail.com", name = "olatejulian"}]
dependencies = ["typer>=0.15.2", "rich>=14.0.0", "pathspec>=0.12.1"]
description = "cli for simple list directory contents"
license = {text = "MIT"}
name = "pyls"
readme = "README.md"
requires-python = ">=3.12,<3.13"
version = "0.1.0"

[tool.pdm]
distribution = true

[tool.pdm.scripts]
cli = {call = "pyls.__main__:main"}
compile = {cmd = "pyinstaller -Fyn pyls pyls/__main__.py"}

[tool.pdm.dev-dependencies]
dev = ["pyinstaller>=6.10.0"]

```

