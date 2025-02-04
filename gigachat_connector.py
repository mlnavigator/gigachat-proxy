import os
from typing import List, Dict, Any
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import time

from config import (gigachat_api_key, gigachat_model, gigachat_scope, gigachat_base_url,
                    gigachat_profanity_check, external_api_resp_timeout, api_delay)
from api_logger import error_logger, error_logger_lock

giga = GigaChat(
    credentials=gigachat_api_key,
    scope=gigachat_scope,
    base_url=gigachat_base_url,
    verify_ssl_certs=False,
    timeout=external_api_resp_timeout,
)

GIGA_PARAMS = {'temperature': 1,  # 0.1
               'top_p': 0,  # 0.1,
               'repetition_penalty': 1,  # 1.1,
               'max_tokens': 2000,
               'model': gigachat_model,
               'profanity_check': gigachat_profanity_check,
               }


def validate_data(data: Dict[str, Any]) -> bool:
    required_fields = {
        "messages": list,
        "generate_parameters": (dict, type(None)),
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            raise ValueError(f"'{field}' is required in data")

        if not isinstance(data[field], expected_type):
            raise TypeError(f"'{field}' should be of type {expected_type}, got {type(data[field])}")

    # Дополнительная проверка для 'messages'
    for message in data["messages"]:
        if not (isinstance(message, (list, tuple)) and len(message) == 2):
            raise ValueError("Каждое сообщение должно быть кортежем/списком из 2 элементов: (role, text)")
        role, text = message
        if not isinstance(role, str) or not isinstance(text, str):
            raise TypeError("В сообщениях, оба элемента должны быть строками")

    return True


def request_api(data: Dict[str, Any], timeout, retry: int=3) -> Dict[str, Any]:
    """
    :param data:
    :param timeout
    :param retry
    :return:

    data['messages']: List[Tuple[str, str]]
    data['generate_parameters']: Dict[str, Any]|None
    """
    retry = int(retry)
    retry = max(retry, 1)

    validate_data(data)

    params = data.get('generate_parameters', {})
    for k,v in GIGA_PARAMS.items():
        if k not in params:
            params[k] = v

    messages = []
    for message in data['messages']:
        role = message[0]
        text = message[1]
        if role == 'system':
            messages.append(Messages(role=MessagesRole.SYSTEM, content=text))
        elif role == 'user':
            messages.append(Messages(role=MessagesRole.USER, content=text))
        elif role == 'assistant':
            messages.append(Messages(role=MessagesRole.ASSISTANT, content=text))
        else:
            raise ValueError(f"Unknown role: {role}")


    payload = Chat(messages=messages, params=params)
    err = None
    for _ in range(retry):
        try:
            response = giga.chat(payload)
            err = None
            break
        except Exception as e:
            with error_logger_lock:
                error_logger.debug(f"Error in request_api: {e}")
            err = e
            time.sleep(api_delay)
            continue

    if err is not None:
        raise err

    return response.dict()


def get_info():
    res = giga.get_models().dict()
    ret = dict()
    ret['default-model'] = gigachat_model
    ret['avail-models'] = res
    return ret

