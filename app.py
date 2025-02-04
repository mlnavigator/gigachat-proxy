import json
import traceback
from bottle import request, response, Bottle
import bottle

from proxy_request import make_request, get_info
from api_logger import error_logger, error_logger_lock
from config import (app_name, host, port, workers, threads_cnt, worker_connections,
                    timeout, debug, max_request_body_size)

bottle.BaseRequest.MEMFILE_MAX = max_request_body_size
app = Bottle()


@app.post('/')
def req():
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    res_data = {'app': app_name, 'status': '', 'data': {}}
    try:
        data = request.json
        if data is None:
            raise ValueError("Empty or invalid JSON")
    except Exception as e:
        data = request.body.read()
        err_message = f'Error while parsing request body: {str(e)}'
        with error_logger_lock:
            error_logger.error(err_message)
            error_logger.error(traceback.format_exc())
            error_logger.error(data)
        response.status = 400
        res_data['status'] = err_message

        return json.dumps(res_data, ensure_ascii=False)

    try:
        # print('received data', data)
        res = make_request(data)
        res_data['status'] = 'ok'
        res_data['data'] = res
        # print({'in': data, 'out': res_data})
        response.status = 200
    except Exception as e:
        res_data['status'] = str(e)
        res_data['data'] = {}
        response.status = 500
        error_trace = traceback.format_exc()
        error_message = {
            'input_data': data,
            'error_trace': error_trace,
            'error_message': str(e)
        }
        error_message = json.dumps(error_message, ensure_ascii=False)
        with error_logger_lock:
            error_logger.error(error_message)

    return json.dumps(res_data, ensure_ascii=False)


@app.get('/')
def index():
    info = get_info()
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp = {'app': app_name, 'status': 'ok', 'info': info}
    return json.dumps(resp, ensure_ascii=False)


def main():
    app.run(host=host, port=port, debug=debug, server='gunicorn', workers=workers, reload=False,
            threads=threads_cnt, timeout=timeout,
            worker_class='gthread',
            worker_connections=worker_connections
            )


if __name__ == '__main__':
    main()
