from typing import List, Tuple, Union, Dict
import os

import requests

gigachat_connect_web_url = os.environ.get('GIGACHAT_CONNECT_WEB_PROXY')
gigachat_connect_web_timeout = os.environ.get('GIGACHAT_CONNECT_WEB_PROXY_TIMEOUT')
if gigachat_connect_web_timeout is not None:
    gigachat_connect_web_timeout = int(gigachat_connect_web_timeout)

model_name = os.environ.get("GIGACHAT_MODEL_NAME")
if model_name is None:
    model_name = "GigaChat-Max"

print('gigachat_connect_web_url: ', gigachat_connect_web_url,
      'gigachat_connect_web_timeout: ', gigachat_connect_web_timeout,
      'model_name: ', model_name)


class GigaChatWebConnector:
    def __init__(self, *args, **kwargs):
        pass

    def chat(self, messages: List[Tuple[str, str]], max_tokens: Union[int, None] = None, retry_cnt: int = 2) -> str:
        """

        :param messages:
        :param max_tokens:
        :param retry_cnt:
        :return:
        """
        retry_cnt = int(retry_cnt)
        retry_cnt = max(retry_cnt, 1)

        max_tokens = 2200 if max_tokens is None else max_tokens

        req_data = {
            'messages': messages,
            'generate_parameters': {'temperature': 1,
               'top_p': 0,
               'repetition_penalty': 1,
               'max_tokens': max_tokens,
               'model': model_name,
               'profanity_check': False,
               }
        }

        data = {}
        for _ in range(retry_cnt):
            try:
                response = requests.post(gigachat_connect_web_url, json=req_data, timeout=gigachat_connect_web_timeout)
                resp_data = response.json()
                # print(resp_data)
                if response.status_code == 200:
                    data = resp_data['data']
                    error = None
                else:
                    data = {}
                    error = resp_data['status']

                if error:
                    print(resp_data)
                break
            except Exception as e:
                print(e)
                data = {}

        res = data['choices'][0]['message']['content'] if data != {} else 'Подключение к Gigachat не удалось'
        return res


if __name__ == '__main__':
    gigachat = GigaChatWebConnector()
    messages = [('system', 'Ты робот киска, на все вопросы отвечай мяу-мяу'),
                ('user', 'Привет, как дела?')]
    text_answer = gigachat.chat(messages, retry_cnt=3)
    print(text_answer)
