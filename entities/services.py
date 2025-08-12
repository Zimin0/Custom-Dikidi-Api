from dataclasses import dataclass, field

from entities.masters import Master
from utils import DikidiApiClient
from logger_init import logger

@dataclass
class Service:
    """
    Represents a service offered by a company, including details and available specialists.

    Attributes:
        id (int): Unique identifier of the service.
        company_service_id (int): Identifier used by the company for internal referencing (from 'company_service_id' in API).
        image (str): URL or path to the image associated with the service (from 'image' in API).
        cost (int): Cost or price of the service (from 'cost' or 'price' in API).
        name (str): Display name of the service (from 'name' in API).
        duration (int): Duration of the service in minutes (mapped from 'time' in API).
        service_value (str): Alternative or duplicate name of the service (from 'service_value' in API).
        service_points (float): Points or rating associated with the service (from 'service_points' in API).
        masters (list[Master]): List of specialists (masters) who can perform this service (fetched separately).
    """
    
    # these attributes will be parsed with parent API entity (Service).
    id: int
    company_service_id: int     # 'company_service_id' in API
    image: str                  # 'image' in API
    cost: int                   # 'cost' or 'price' in API
    name: str                   # 'name' in API
    duration: int = 0           # 'time' in API
    service_value: str = ""     # duplicates 'name' field, 'service_value' in value
    service_points: float = 0.0 # 'service_points' in API

    # these attributes must be collected separately.
    masters: list[Master] = field(default_factory=list)

    def __str__(self):
        return f"Service № {self.id} | '{self.name}'"
