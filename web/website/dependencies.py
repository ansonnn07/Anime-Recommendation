from injector import singleton
from .embedding_model import Model, InitializedModel


def configure(binder):
    binder.bind(Model, to=Model, scope=singleton)
    binder.bind(InitializedModel, to=InitializedModel, scope=singleton)
