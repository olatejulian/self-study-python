from typing import Protocol


class DFSCommand(Protocol): ...


class SkipChildren(DFSCommand): ...


class StopTraversal(DFSCommand): ...
