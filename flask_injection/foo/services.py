from typing import Protocol


class FooService(Protocol):
    def __init__(self, name: str, **kwargs) -> None:
        ...

    def foobobulate(self, greeting: str) -> bool:
        """Does something with string and returns success status."""
        ...


class FooServiceImpl(FooService):
    def __init__(self, name: str, **kwargs) -> None:
        self._name = name

    def _call_third_party(self) -> None:
        print("Calling third party...")

    def foobobulate(self, greeting: str) -> bool:
        self._call_third_party()
        print(f"A side-effect from real impl {self._name}!\n\t{greeting}")
        return True
