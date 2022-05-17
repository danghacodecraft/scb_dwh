import logging
from config.settings import DEBUG


def logger(string, log_name='service', type='error'):
    if not DEBUG:
        logger = logging.getLogger(log_name)

        file_log_handler = logging.FileHandler('media/log/{}.log'.format(log_name))

        logger.addHandler(file_log_handler)

        formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(message)s')
        file_log_handler.setFormatter(formatter)

        if type == 'info':
            logger.info(string)
        elif type == 'error':
            logger.error(string)

        logger.handlers.pop()
    else:
        print(string)
