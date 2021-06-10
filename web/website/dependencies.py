from injector import singleton
from .embedding_model import InitializedModel


def configure(binder):
    binder.bind(InitializedModel, to=InitializedModel, scope=singleton)
