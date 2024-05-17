import pytest
from assertpy import assert_that
from pytest_mock import MockerFixture

from tests.builders.config_builder import ConfigBuilder

from user.config import Config


@pytest.mark.describe(Config.__name__)
class TestConfig:
    @pytest.mark.it("Should create config successfully")
    def test_create_config(self, mocker: MockerFixture) -> None:
        # given
        config_values = ConfigBuilder().build()
        num_config_values = len(config_values.keys())
        exit_mock = mocker.patch("sys.exit")
        getenv_mock = mocker.patch("os.getenv")
        getenv_mock.side_effect = config_values.get

        # when
        Config.from_env()

        # then
        assert_that(getenv_mock.call_count).is_equal_to(num_config_values)
        exit_mock.assert_not_called()

    @pytest.mark.it("Should exit with return code 1")
    def test_exit_code_one(self, mocker: MockerFixture) -> None:
        # given
        exit_mock = mocker.patch("sys.exit")
        getenv_mock = mocker.patch("os.getenv")
        getenv_mock.return_value = None

        # when
        Config.from_env()

        # then
        exit_mock.assert_called_once_with(1)
        getenv_mock.assert_called()
