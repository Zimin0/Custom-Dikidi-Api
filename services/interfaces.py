from abc import ABC, abstractmethod
from utils import DikidiApiClient 

class IParsingService(ABC):
    """ Interface for producing various entities's parsing services. """

    def __init__(self, client: DikidiApiClient):
        self.client = client

    @abstractmethod
    def get_all_objects(self):
        raise NotImplementedError
