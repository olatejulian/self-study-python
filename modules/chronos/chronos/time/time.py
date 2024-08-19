from __future__ import annotations

from decimal import Decimal


class Time:
    __HOUR_TO_MILLISECOND_CONVERSION_FACTOR = Decimal(3600000.000000000)
    __MINUTE_TO_MILLISECOND_CONVERSION_FACTOR = Decimal(60000.000000000)
    __SECOND_TO_MILLISECOND_CONVERSION_FACTOR = Decimal(1000.000000000)

    def __init__(self, milliseconds: Decimal | float = Decimal()):
        self.__milliseconds = Decimal(milliseconds)

    def __add__(self, other: Time) -> Time:
        self.__milliseconds += other._dec_ms

        return self

    def __sub__(self, other: Time) -> Time:
        self.__milliseconds -= other._dec_ms

        return self

    @classmethod
    def of(
        cls,
        hours: float = 0,
        minutes: float = 0,
        seconds: float = 0,
        milliseconds: float = 0,
    ) -> Time:
        return Time(
            (Decimal(hours) * cls.__HOUR_TO_MILLISECOND_CONVERSION_FACTOR)
            + (
                Decimal(minutes)
                * cls.__MINUTE_TO_MILLISECOND_CONVERSION_FACTOR
            )
            + (
                Decimal(seconds)
                * cls.__SECOND_TO_MILLISECOND_CONVERSION_FACTOR
            )
            + Decimal(milliseconds)
        )

    @property
    def in_hours(self) -> Decimal:
        return (
            self.__milliseconds / self.__HOUR_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def in_minutes(self) -> Decimal:
        return (
            self.__milliseconds
            / self.__MINUTE_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def in_seconds(self) -> Decimal:
        return (
            self.__milliseconds
            / self.__SECOND_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def in_milliseconds(self) -> Decimal:
        return self.__milliseconds

    @property
    def hours(self) -> int:
        return int(
            self.__milliseconds // self.__HOUR_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def minutes(self) -> int:
        return int(
            self.__milliseconds
            // self.__MINUTE_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def seconds(self) -> int:
        return int(
            self.__milliseconds
            // self.__SECOND_TO_MILLISECOND_CONVERSION_FACTOR
        )

    @property
    def milliseconds(self) -> int:
        return int(self.__milliseconds)

    @property
    def _dec_ms(self) -> Decimal:
        return self.__milliseconds
