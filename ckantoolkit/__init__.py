from contextlib import contextmanager
from contextvars import ContextVar

# Config only needs to respond to get and update 
context = ContextVar("config", default={})

class ContextConfig:
    def __init__(self, context):
        self.context = context

    @contextmanager
    def parameterize(self, value):
        token = self.context.set(value)
        try:
            yield self
        finally:
            self.context.reset(token)

    def get(self, *args):
        config = self.context.get()
        return config.get(*args)

    def update(self, *args):
        config = self.context.get()
        ret = config.update(*args)
        return ret

config = ContextConfig(context)

h = False
