import argon2
from injector import Binder, Injector, Module, multiprovider, provider, singleton

from user.app import App
from user.common import Controller
from user.config import Config
from user.domain.repositories import UserRepository
from user.domain.services import PasswordHasher
from user.domain.use_cases import CreateUserUseCase
from user.infra.controllers import CreateUserController, HealthzController
from user.infra.repositories.mongo import MongoUserRepository
from user.infra.repositories.mongo.models import UserMongo
from user.infra.services import Argon2PasswordHasher
from user.types import BeanieParams, DocumentModel


class UserModule(Module):
    _controllers: list[type[Controller]] = [
        CreateUserController,
        HealthzController,
    ]
    _document_models: list[DocumentModel] = [
        UserMongo,
    ]

    @singleton
    @multiprovider
    def provide_controllers(
        self,
        injector: Injector,
    ) -> list[Controller]:
        return [injector.get(klass) for klass in self._controllers]

    @singleton
    @provider
    def provide_beanie_params(self) -> BeanieParams:
        return {
            "database": "user",
            "document_models": self._document_models,
        }

    def configure(self, binder: Binder) -> None:
        # Config
        binder.bind(Config, to=Config.from_env, scope=singleton)

        # Services
        binder.bind(argon2.PasswordHasher, to=argon2.PasswordHasher, scope=singleton)
        binder.bind(PasswordHasher, to=Argon2PasswordHasher, scope=singleton)

        # Repositories
        binder.bind(UserRepository, to=MongoUserRepository, scope=singleton)

        # Use cases
        binder.bind(CreateUserUseCase, to=CreateUserUseCase, scope=singleton)

        # Controllers
        for controller in self._controllers:
            binder.bind(controller, to=controller, scope=singleton)

        binder.bind(App, to=App, scope=singleton)
