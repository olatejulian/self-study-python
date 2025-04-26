from __future__ import annotations

from statistics import mean


class Color:
    def __init__(self, red: float, green: float, blue: float):
        if (
            self.__validate_color_value(red)
            and self.__validate_color_value(green)
            and self.__validate_color_value(blue)
        ):
            self.__red = red
            self.__green = green
            self.__blue = blue

        else:
            raise ValueError("All color values must be between 0 and 255.")

    def __repr__(self):
        return self.__color_text(
            self.__red,
            self.__green,
            self.__blue,
            f"Color(red={self.__red},green={self.__green},blue={self.__blue})",
        )

    def __str__(self):
        return self.__color_text(
            self.__red,
            self.__green,
            self.__blue,
            self.__to_rgb_string(self.__red, self.__green, self.__blue),
        )

    def __add__(self, other: Color) -> Color:
        other_red_value, other_green_value, other_blue_value = (
            other.get_colors()
        )

        new_red = mean([other_red_value, self.__red])
        new_green = mean([other_green_value, self.__green])
        new_blue = mean([other_blue_value, self.__blue])

        return Color(new_red, new_green, new_blue)

    @staticmethod
    def __validate_color_value(color_value: float) -> bool:
        return 0 <= color_value <= 255

    @staticmethod
    def __to_hexadecimal_string(red: float, green: float, blue: float) -> str:
        return f"#{round(red):02x}{round(green):02x}{round(blue):02x}".upper()

    @staticmethod
    def __to_rgb_string(red: float, green: float, blue: float) -> str:
        return f"rgb({red}, {green}, {blue})"

    @staticmethod
    def __color_text(red: float, green: float, blue: float, text: str) -> str:
        red, green, blue = int(red), int(green), int(blue)
        return f"\033[38;2;{red};{green};{blue}m{text}\033[0m"

    @classmethod
    def from_rgb_string(cls, rgb_string: str) -> Color:
        red, green, blue = (
            rgb_string.replace("rgb(", "").replace(")", "").split(",")
        )
        return cls(float(red), float(green), float(blue))

    @classmethod
    def from_hexadecimal_string(cls, hexadecimal_string: str) -> Color:
        red, green, blue = (
            int(hexadecimal_string[1:3], 16),
            int(hexadecimal_string[3:5], 16),
            int(hexadecimal_string[5:], 16),
        )
        return cls(red, green, blue)

    @property
    def rgb(self):
        return self.__to_rgb_string(self.__red, self.__green, self.__blue)

    @property
    def hex(self):
        return self.__to_hexadecimal_string(
            self.__red, self.__green, self.__blue
        )

    def get_colors(self) -> tuple[float, float, float]:
        return self.__red, self.__green, self.__blue

    def show(self, print_format: str = "rgb") -> None:
        match print_format:
            case "hex":
                print(
                    self.__color_text(
                        self.__red,
                        self.__green,
                        self.__blue,
                        self.__to_hexadecimal_string(
                            self.__red, self.__green, self.__blue
                        ),
                    )
                )

            case "rgb":
                print(str(self))

            case _:
                raise ValueError
