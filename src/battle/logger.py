import logging
import json
LOGGER = {}


def make_battle_logger(env, log):
    logger = logging.getLogger(str(env))
    handler = ListHandler(log)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    LOGGER[env] = logger


def make_battle_record(time, action, champion, **kwargs):
    result = {
        "time": time,
        "action": action,
        "champion": champion
    }
    for v in kwargs.keys():
        result[v] = kwargs[v]
    return result


class ListHandler(logging.Handler):
    def __init__(self, log):
        super(ListHandler, self).__init__()
        self.log = log

    def emit(self, record: logging.LogRecord) -> None:
        self.log.append(json.dumps(record.msg))
        self.flush()
