from config import core
from foo.tests import fakes as foo_fakes


class Config(core.Config):
    NAME = "test flask app"

    # Injectables
    FOO_SERVICE_IMPL = foo_fakes.FooServiceFake
