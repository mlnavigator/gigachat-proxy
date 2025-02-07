from dotenv import load_dotenv
import os

base_path = os.path.dirname(__file__)
env_path = os.path.join(base_path, 'assets', 'env')
load_dotenv(env_path)

# app params
host = os.environ.get('HOST', '0.0.0.0').strip()
port = int(os.environ.get('PORT', '8078').strip())
workers = 1
threads_cnt = int(os.environ.get('THREADS', '20').strip())
worker_connections = 200
timeout = int(os.environ.get('RESP_TIMEOUT', '300').strip())  # Ответ от нашего сервиса
debug = bool(int(os.environ.get('APP_DEBUG', True)))
max_request_body_size = 1024 * 1024 * 10
app_name = os.environ['APP_NAME'].strip()

# Настройки логирования из переменных окружения
log_level = os.environ.get("LOG_LEVEL", "DEBUG").strip().upper()  # По умолчанию DEBUG
error_log_file = os.environ.get("LOG_FILE", os.path.join(base_path, 'assets', 'api_log.jsonl')).strip()  # Имя файла логов
requests_log_file = os.environ.get("REQUESTS_LOG_FILE", os.path.join(base_path, 'assets', "requests_log.jsonl")).strip()  # Имя файла логов
log_max_bytes = 50 * 1024 * 1024                           # Максимальный размер файла логов в байтах
log_backup_count = 3

# параметры лимитов для обращения к внешнему API
external_api_resp_timeout = int(os.environ['EXP_RESP_TIMEOUT'].strip())
external_api_rpm = float(os.environ['EXT_API_RPM'].strip())
api_delay = 60 / external_api_rpm
external_max_requests = int(os.environ['EXT_MAX_REQUESTS'].strip())

# env variables for external api
gigachat_api_key = os.environ['GIGACHAT_API_KEY'].strip()
gigachat_model = os.environ['GIGACHAT_MODEL'].strip()
gigachat_scope = os.environ.get('GIGACHAT_SCOPE', None)
gigachat_base_url = os.environ.get('GIGACHAT_BASE_URL', None)
gigachat_profanity_check = bool(os.environ.get('GIGACHAT_PROFANITY_CHECK', '1').strip())
