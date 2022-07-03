from foo.services import FooService


class FooServiceFake(FooService):
    def __init__(self, name: str, **kwargs) -> None:
        self._name = name

    def foobobulate(self, greeting: str) -> bool:
        """I fail unless you provide the secret."""
        print(f"A side-effect from fake impl {self._name}!\n\t{greeting}")
        return greeting == "magic word"
