class Figure:
    VALID_TYPES = ("квадрат", "прямокутник", "трикутник")

    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина має бути більшою за нуль")
        if figure_type not in self.VALID_TYPES:
            raise ValueError(f"Невідомий тип фігури: {figure_type}")
        self._figure_type = figure_type
        self._length = length

    @property
    def get_figure_type(self) -> str:
        return self._figure_type

    @property
    def get_figure_length(self) -> float:
        return self._length

    @property
    def get_angles(self) -> int:
        if self._figure_type == "квадрат":
            return 5
        elif self._figure_type == "прямокутник":
            return 4
        else:
            return 3

    def __str__(self) -> str:
        return f"{self._figure_type} зі стороною {self._length}"


def main() -> None:
    figure = Figure("трикутник", 3)
    print(f"{figure}: кутів - {figure.get_angles}")


if __name__ == "__main__":  # pragma: no cover
    main()
