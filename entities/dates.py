from dataclasses import dataclass, field

@dataclass
class Dates:
    """
    Класс для хранения информации о доступных датах и времени записи для мастера.

    Attributes:
        dates_true (list[str]): Список доступных дат.
        date_near (str): Ближайшая доступная дата.
        times (list[str]): Доступные временные интервалы для записи.
        first_date_true (str): Первая доступная дата.
    """
    dates_true: list[str] = field(default_factory=list)
    date_near: str = ""
    times: list[str] = field(default_factory=list)
    first_date_true: str = ""
