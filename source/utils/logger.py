import logging, os

log_counter = 1

log_filename = f'source/data/logs/bot_log{log_counter}.log'

while os.path.exists(log_filename):
    log_counter += 1
    log_filename = f'source/data/logs/bot_log{log_counter}.log'

file_log = logging.FileHandler(log_filename)
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Пример использования логирования
logging.info("Логирование запущено.")