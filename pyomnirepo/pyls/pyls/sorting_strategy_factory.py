from enum import StrEnum

from .sorting_strategy import (
    SortByAccessDate,
    SortByCreationDate,
    SortByModificationDate,
    SortByName,
    SortingStrategy,
)


class SortBy(StrEnum):
    NAME = "name"
    ACCESS_DATE = "access_date"
    CREATION_DATE = "creation_date"
    MODIFICATION_DATE = "modification_date"


class SortByStrategyFactory:
    @staticmethod
    def create(sort_by: SortBy) -> SortingStrategy:
        strategies = {
            SortBy.NAME: SortByName(),
            SortBy.ACCESS_DATE: SortByAccessDate(),
            SortBy.CREATION_DATE: SortByCreationDate(),
            SortBy.MODIFICATION_DATE: SortByModificationDate(),
        }

        return strategies[sort_by]
