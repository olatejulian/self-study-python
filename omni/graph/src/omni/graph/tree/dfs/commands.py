from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DFSCommand: ...


@dataclass(slots=True, frozen=True)
class SkipChildren(DFSCommand): ...


@dataclass(slots=True, frozen=True)
class StopTraversal(DFSCommand): ...
