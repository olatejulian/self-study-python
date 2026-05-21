from collections.abc import Callable
from enum import StrEnum

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
