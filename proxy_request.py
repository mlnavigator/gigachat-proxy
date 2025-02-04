import time
from typing import Callable, List, Dict, Any, Union
from threading import Lock
import json
from concurrent.futures import ThreadPoolExecutor

from api_logger import error_logger, requests_logger, error_logger_lock, requests_logger_lock
from gigachat_connector import validate_data, request_api, get_info
from config import external_api_resp_timeout, api_delay, external_max_requests

last_call = 0

lock_main = Lock()

tp = ThreadPoolExecutor(max_workers=external_max_requests)

def control_delay():
    global last_call

    with lock_main:
        t0 = time.time()
        delta = t0 - last_call
        if delta < api_delay:
            to_wait = api_delay - delta
            time.sleep(to_wait)
            last_call = time.time()


def get_response(data, timeout=external_api_resp_timeout) -> Dict[str, Any]:
    t0 = time.time()
    control_delay()
    t1 = time.time()
    err = None
    try:
        ret = request_api(data, timeout=timeout)
    except Exception as e:
        ret = {'error': str(e)}
        err = e

    time_exec = time.time() - t1
    wait_time = t1 - t0
    call_stat = dict()
    call_stat['time_exec'] = time_exec
    call_stat['wait_time'] = wait_time
    call_stat['data'] = data
    call_stat['res'] = ret

    with requests_logger_lock:
        requests_logger.debug(json.dumps(call_stat, ensure_ascii=False))

    if err is not None:
        raise err

    return ret


def make_request(data, timeout=external_api_resp_timeout) -> Dict[str, Any]:
    validate_data(data)
    f = tp.submit(get_response, data, timeout)
    res = f.result()
    return res
