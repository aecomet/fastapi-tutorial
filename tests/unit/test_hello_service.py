from app.services.hello import build_hello_message


def test_build_hello_message_default():
    """引数なしで 'Hello World' を返すこと"""
    result = build_hello_message()
    assert result == {"message": "Hello World"}


def test_build_hello_message_with_name():
    """name を指定すると 'Hello {name}' を返すこと"""
    result = build_hello_message("FastAPI")
    assert result == {"message": "Hello FastAPI"}


def test_build_hello_message_returns_dict():
    """戻り値が dict であること"""
    result = build_hello_message()
    assert isinstance(result, dict)
    assert "message" in result
