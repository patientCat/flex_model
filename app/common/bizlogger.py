# 创建日志记录器
import logging
import uuid
from datetime import datetime

from pythonjsonlogger import jsonlogger

from app.common.thread_local_utils import BIZ_CONTEXT


# 将日志处理器添加到日志记录器
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        trace = self._get_trace_id()
        if trace:
            log_record["trace_id"] = trace

        request_id = self._get_request_id()
        if request_id:
            log_record["request_id"] = request_id

    def _get_trace_id(self):
        return BIZ_CONTEXT.get_attr_and_set("trace_id", uuid.uuid4().hex)

    def _get_request_id(self):
        return BIZ_CONTEXT.get_attr("request_id")

    def _get_project_id(self):
        return BIZ_CONTEXT.get_attr("project_id")


LOGGER: logging.Logger = logging.getLogger("app")


def init_logger():
    LOGGER.setLevel(logging.INFO)

    # 创建日志处理器
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(request_id)s %(trace_id)s %(project_id)s %(filename)s %(lineno)d %(message)s')

    # 创建日志格式器
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


@property
def get_logger() -> logging.Logger:
    logger = logging.getLogger("app")
    return logger
