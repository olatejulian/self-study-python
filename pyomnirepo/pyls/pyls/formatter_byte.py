from abc import ABC, abstractmethod


class ByteFormatter(ABC):
    @abstractmethod
    def __call__(self, size_in_bytes: int) -> str:
        pass


class DefaultByteFormatter:
    KILOBYTES_DIVISOR = 1024
    MEGABYTES_DIVISOR = 1024**2
    GIGABYTES_DIVISOR = 1024**3

    def __call__(self, size_in_bytes: int) -> str:
        return self.__format_size(size_in_bytes)

    def __format_size(self, size_in_bytes: int) -> str:
        if 0 <= size_in_bytes < self.KILOBYTES_DIVISOR:
            return f"{self.__to_kilobytes(size_in_bytes):.2f}B"

        if self.KILOBYTES_DIVISOR <= size_in_bytes < self.MEGABYTES_DIVISOR:
            return f"{self.__to_megabytes(size_in_bytes):.2f}MB"

        return f"{self.__to_gigabytes(size_in_bytes):.2f}GB"

    def __to_kilobytes(self, size_in_bytes: int) -> float:
        return size_in_bytes / self.MEGABYTES_DIVISOR

    def __to_megabytes(self, size_in_bytes: int) -> float:
        return size_in_bytes / self.MEGABYTES_DIVISOR

    def __to_gigabytes(self, size_in_bytes: int) -> float:
        return size_in_bytes / self.GIGABYTES_DIVISOR
