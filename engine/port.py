from abc import ABC, abstractmethod


class ToolPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def apply(self, palette: dict, is_dark: bool) -> bool:
        ...

    def reload(self) -> None:
        pass
