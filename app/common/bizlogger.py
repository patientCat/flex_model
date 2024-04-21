# 创建日志记录器
import logging
import uuid
from datetime import datetime
from typing import Any

from pythonjsonlogger import jsonlogger

from app.common.thread_local_utils import BIZ_CONTEXT


class LogKey:
    request_id = "request_id"
    project_id = "project_id"
    action = "action"
    trace_id = "trace_id"


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

        self.set_key_of_log_record(log_record, LogKey.trace_id, self._get_trace_id())
        self.set_key_of_log_record(log_record, LogKey.request_id, self._get_request_id())
        self.set_key_of_log_record(log_record, LogKey.project_id, self._get_project_id())
        self.set_key_of_log_record(log_record, LogKey.action, self._get_action())

    def set_key_of_log_record(self, log_record: dict, key: str, value: Any):
        log_record[key] = value if value else ""

    def _get_trace_id(self):
        return BIZ_CONTEXT.get_attr_and_set(LogKey.trace_id, uuid.uuid4().hex)

    def _get_request_id(self):
        return BIZ_CONTEXT.get_attr(LogKey.request_id)

    def _get_project_id(self):
        return BIZ_CONTEXT.get_attr(LogKey.project_id)

    def _get_action(self):
        return BIZ_CONTEXT.get_attr(LogKey.action)


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
