from dataclasses import dataclass
from abc import abstractmethod
from enum import Enum

class Package_Tag(Enum):
    Pages = 1
    FullText = 2

@dataclass()
class Txt_package():
    txt: [str]
    interest_score: float
    tag: [Package_Tag]


class Pipeline_Actor:
    @abstractmethod
    def get_packages(self) -> [Txt_package]:
        pass
        # Каждый элемент пайплайна должен возвращать пакеты с текстами