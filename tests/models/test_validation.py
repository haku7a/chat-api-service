import pytest
from pydantic import ValidationError
from app.models.chat import Chat
from app.models.message import Message


def test_chat_title_trimming():
    chat = Chat(title="  trimmed title  ")
    assert chat.title == "trimmed title"


def test_message_text_trimming():
    message = Message(text="  trimmed message  ")
    assert message.text == "trimmed message"


def test_chat_title_too_long():
    long_title = "a" * 256
    with pytest.raises(ValidationError):
        Chat(title=long_title)


def test_message_text_too_long():
    long_text = "a" * 5001
    with pytest.raises(ValidationError):
        Message(text=long_text)


def test_chat_title_empty():
    with pytest.raises(ValidationError):
        Chat(title="   ")


def test_message_text_empty():
    with pytest.raises(ValidationError):
        Message(text="   ")
