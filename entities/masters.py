from dataclasses import dataclass, field

from entities.dates import Date
from utils import DikidiApi
from logger_init import logger

@dataclass
class Master:
    """
    Represents a specialist (master) who provides a specific service.

    Attributes:
        id (int): Unique identifier of the master.
        name (str): Display name of the master (mapped from 'username' in API).
        service_name (str): Name of the service provided by the master.
        duration (int): Duration of the service in minutes (mapped from 'time' in API).
        free_dates (list[str]): Available dates for booking the master (mapped from 'dates_true' in API).
        dates (list[Date]): Detailed information for each available date (should be fetched separately).
    """
    
    # these attributes will be parsed with parent API entity (Master).
    id: int
    name: str                                           # 'username' in API
    service_name: str = ""                              # 'service_name' in API
    duration: int = 0                                   # 'time' in API
    free_dates: list[str] = field(default_factory=list) # 'dates_true' in API
    
    # these attributes must be collected separately.
    dates: list[Date] = field(default_factory=list)

    def __str__(self):
        return f"Master № {self.id} | '{self.username}'"

