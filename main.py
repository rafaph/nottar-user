import src.logger  # noqa: F401, I001

from injector import Injector

from src.app import App
from src.user_module import UserModule

if __name__ == "__main__":
    try:
        from pytest_cov.embed import cleanup_on_sigterm  # type: ignore
    except ImportError:
        pass
    else:
        cleanup_on_sigterm()

    injector = Injector([UserModule()])
    app = injector.get(App)
    app.run()
