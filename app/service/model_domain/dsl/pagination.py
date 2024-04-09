from dataclasses import dataclass
from typing import Optional

from app.common.error import BizException, ErrorCode


@dataclass
class Pagination:
    limit: int = 10
    offset: int = 0


class PaginationFactory:
    ERROR_MESSAGE_INVALID_LIMIT = "limit must be greater than 0"
    ERROR_MESSAGE_INVALID_OFFSET = "offset must be greater than equal 0"

    KEY_LIMIT = "limit"
    KEY_OFFSET = "offset"

    def create_pagination(self, param_dict: dict) -> Pagination:
        limit = param_dict.get(self.KEY_LIMIT)
        offset = param_dict.get(self.KEY_OFFSET)

        return self._create_pagination(limit, offset)

    def create_one_pagination(self) -> Pagination:
        limit = 1
        offset = 0
        return self._create_pagination(limit, offset)

    def _create_pagination(self, limit: Optional[int], offset: Optional[int]) -> Pagination:
        if limit is None:
            limit = 10
        if offset is None:
            offset = 0
        if limit < 0:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_MESSAGE_INVALID_LIMIT)
        if offset < 0:
            raise BizException(ErrorCode.InvalidParameter, self.ERROR_MESSAGE_INVALID_OFFSET)

        return Pagination(limit=limit, offset=offset)
