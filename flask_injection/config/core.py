from abc import ABCMeta

from foo import services as foo_services


class Config(metaclass=ABCMeta):
    NAME = "flask_config_injection"

    # Injectables
    FOO_SERVICE_IMPL = foo_services.FooServiceImpl
