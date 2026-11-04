from unittest.mock import Mock, patch

from sagery.engine import get_async_engine


@patch("sagery.engine.create_async_engine")
def test_get_async_engine(create_async_engine_mock: Mock) -> None:
    settings = Mock()

    engine = get_async_engine(settings)

    settings.url.unicode_string.assert_called_once_with()
    create_async_engine_mock.assert_called_once_with(settings.url.unicode_string.return_value)
    assert engine is create_async_engine_mock.return_value
