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
        angles = {
            "квадрат": 4,
            "прямокутник": 4,
            "трикутник": 3,
        }
        return angles[self._figure_type]

    def __str__(self) -> str:
        return f"{self._figure_type} зі стороною {self._length}"