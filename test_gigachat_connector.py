import config
from gigachat_connector import request_api, validate_data

import pytest


def test_request_api():
    model = 'GigaChat-Max'
    data = {
        "messages": [
            ("system", "You are a helpful assistant."),
            ("user", "Who was the first president of the United States?"),
            ("assistant", "George Washington was the first president of the United States."),
            ("user", "Who is current president of the United States?"),
        ],
        "generate_parameters": {
            "temperature": 0.7,
            "top_p": 0.1,
            "repetition_penalty": 1,
            "max_tokens": 2000,
            "model": model,
            "profanity_check": False,
        }
    }

    response = request_api(data, 10)
    assert response is not None
    assert type(response) is dict
    assert 'choices' in response
    assert 'model' in response
    assert  model in response['model']
    assert type(response["choices"]) is list
    assert len(response) > 0
    assert response['choices'][0]['message']['role'] == 'assistant'


def test_validate_data():
    data = {
        "messages": [
            ("system", "You are a helpful assistant."),
            ("user", "Who was the first president of the United States?"),
            ("assistant", "George Washington was the first president of the United States."),
            ("user", "Who is current president of the United States?"),
        ],
        "generate_parameters": {
            "temperature": 0.7,
            "top_p": 0.1,
            "repetition_penalty": 1,
            "max_tokens": 2000,
            "model": "GigaChat-Max",
            "profanity_check": False
        }
    }

    assert validate_data(data) is True

    data = {}
    with pytest.raises(ValueError):
        validate_data(data)

    data = {'messages': 'privet', 'generate_parameters': ''}
    with pytest.raises(TypeError):
        validate_data(data)


if __name__ == '__main__':
    test_request_api()
    test_validate_data()

