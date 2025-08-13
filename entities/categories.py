from dataclasses import dataclass, field

from entities.services import Service

@dataclass
class Category:
    """
    Represents a category that groups multiple services.

    Attributes:
        id (int): Unique identifier of the category (from 'id' in API).
        name (str): Display name of the category (from 'name' in API).
        category_value (str): Alternative or duplicate name of the category (from 'category_value' in API).
        services (list[Service]): List of services that belong to this category (fetched separately).
    """

    # these attributes will be parsed with parent API entity (Category).
    id: int             # 'id' in API
    name: str           # 'name' in API
    category_value: str # duplicates 'name' field, 'category_value' in API

    # these attributes must be collected separately.
    services: list[Service] = field(default_factory=list)

    def __str__(self):
        return f"Category № {self.id} | '{self.name}'"
