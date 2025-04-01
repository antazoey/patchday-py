import pytest


@pytest.fixture
def mock_data(mocker):
    return mocker.MagicMock()
