import argon2
from injector import Binder, Injector, Module, multiprovider, provider, singleton

from src.app import App
from src.common import Controller
from src.config import Config
from src.domain.repositories import UserRepository
from src.domain.services import PasswordHasher
from src.domain.use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    RetrieveUserUseCase,
    UpdateUserUseCase,
    VerifyUserUseCase,
)
from src.infra.controllers import (
    CreateUserController,
    DeleteUserController,
    HealthzController,
    RetrieveUserController,
    UpdateUserController,
    VerifyUserController,
)
from src.infra.repositories.mongo import MongoUserRepository
from src.infra.repositories.mongo.models import UserMongo
from src.infra.services import Argon2PasswordHasher
from src.types import BeanieParams, DocumentModel


class UserModule(Module):
    _controllers: list[type[Controller]] = [
        CreateUserController,
        DeleteUserController,
        HealthzController,
        RetrieveUserController,
        UpdateUserController,
        VerifyUserController,
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
        binder.bind(DeleteUserUseCase, to=DeleteUserUseCase, scope=singleton)
        binder.bind(RetrieveUserUseCase, to=RetrieveUserUseCase, scope=singleton)
        binder.bind(UpdateUserUseCase, to=UpdateUserUseCase, scope=singleton)
        binder.bind(VerifyUserUseCase, to=VerifyUserUseCase, scope=singleton)

        # Controllers
        for controller in self._controllers:
            binder.bind(controller, to=controller, scope=singleton)

        binder.bind(App, to=App, scope=singleton)
