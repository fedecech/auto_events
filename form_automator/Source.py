from abc import abstractmethod
from typing import List, Optional

from .Event import Event
from .Provider import Provider


class Source:
    def __init__(self, provider: Optional['Provider'] = None) -> None:
        self.provider = provider

    @abstractmethod
    def load_events(self) -> List['Event']:
        ...

    @abstractmethod
    def handle_consent(self, *args, **kwargs):
        ...
