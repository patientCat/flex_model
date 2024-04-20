import json
from typing import Optional, List

import loguru
import pymongo
from bson import json_util

from app.common.error import BizException, ErrorCode
from app.domain.lowcode_model.dsl.dsl_param import IncludeContext, IncludeParam
from app.domain.project_ctx import database
from app.domain.lowcode_model.dsl.dsl_domain import FindDomain, CreateDomain, CreateManyDomain, FindManyDomain, \
    UpdateDomain, UpdateManyDomain, DeleteDomain, DeleteManyDomain
from app.domain.project_ctx.database import DbContext


def remove_oid_and_date(obj):
    print(obj)
    if isinstance(obj, dict):
        if '$oid' in obj:
            return str(obj['$oid'])
        if '$date' in obj:
            return str(obj['$date'])
        return {k: remove_oid_and_date(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [remove_oid_and_date(item) for item in obj]
    return obj


def do_find(collection, pagination, projection, query) -> list:
    cursor: pymongo.cursor.Cursor = collection.find(filter=query, projection=projection, limit=pagination.limit,
                                                    skip=pagination.offset)
    doc_list = []
    for doc in cursor:
        json_doc = json.dumps(doc, sort_keys=True, default=json_util.default)
        dict_doc = json.loads(json_doc)
        doc_list.append(remove_oid_and_date(dict_doc))
    return doc_list


def do_aggregate(collection, projection: dict, query: dict, include_ctx: IncludeContext) -> list:
    pipeline = [
        {'$match': query},
        {'$project': projection},
    ]
    include_param_list: List[IncludeParam] = include_ctx.include_param_list
    for include_param in include_param_list:
        if include_param is None:
            continue
        for mongo_cmd in include_param.to_mongo_cmd_list():
            pipeline.append(mongo_cmd)

    loguru.logger.info(f"aggregate_pipeline={pipeline}")

    cursor: pymongo.cursor.Cursor = collection.aggregate(pipeline=pipeline)
    doc_list = []
    for doc in cursor:
        json_doc = json.dumps(doc, sort_keys=True, default=json_util.default)
        dict_doc = json.loads(json_doc)
        doc_list.append(remove_oid_and_date(dict_doc))
    return doc_list


def do_count(collection, query) -> int:
    total: int = collection.count(filter=query)
    return total


def do_update(collection, query, data, update_many=False) -> int:
    update = {
        "$set": data
    }
    if update_many:
        result = collection.update_many(query, update)
    else:
        result = collection.update_one(query, update)
    return result.modified_count


def do_delete(collection, query, unique: bool, delete_many: bool):
    if unique is True:
        count = collection.count_documents(filter=query)
        if count > 1:
            raise BizException(ErrorCode.InvalidParameter, "to delete record not unique")

    if delete_many:
        result = collection.delete_many(filter=query)
    else:
        result = collection.delete_one(filter=query)
    return result.deleted_count


class MongoRepoService:
    def __init__(self, db_context: DbContext):
        self.db_context: DbContext = db_context

    def _connect_to_db(self):
        # 连接到MongoDB服务器
        client = self.db_context.create_client()

        # 选择一个数据库
        db = client[self.db_context.database_name()]

        # 选择一个集合(类似于表)
        collection = db[self.db_context.col_name()]

        return client, db, collection

    def apply_create(self, create_domain: CreateDomain) -> str:
        client, db, collection = self._connect_to_db()
        loguru.logger.info(f"create data={create_domain.data}")
        collection.insert_one(create_domain.data)
        return str(create_domain.insert_id)

    def apply_create_many(self, create_domain: CreateManyDomain) -> list:
        client, db, collection = self._connect_to_db()
        collection.insert_many(create_domain.datalist)

        return create_domain.insert_id_list

    def apply_find(self, find_domain: FindDomain) -> (Optional[dict], Optional[int]):
        client, db, collection = self._connect_to_db()
        query = find_domain.where_node.to_dict()
        projection = find_domain.selector.select_dict
        # 默认情况下，不返回mongo的_id
        projection["_id"] = 0
        pagination = find_domain.pagination
        include_context = find_domain.include_context
        total = None
        if find_domain.with_count:
            total = do_count(collection, query)
        if find_domain.need_include:
            doc_list = do_aggregate(collection, projection, query, include_context)
        else:
            doc_list = do_find(collection, pagination, projection, query)
        if len(doc_list) == 0:
            return None, total
        else:
            return doc_list[0], total

    def apply_find_many(self, find_many_domain: FindManyDomain) -> (Optional[list], Optional[int]):
        client, db, collection = self._connect_to_db()

        query = find_many_domain.where_node.to_dict()
        projection = find_many_domain.selector.select_dict
        # 默认情况下，不返回mongo的_id
        projection["_id"] = 0
        pagination = find_many_domain.pagination
        include_context = find_many_domain.include_context
        total = None
        if find_many_domain.with_count:
            total = do_count(collection, query)
        if find_many_domain.need_include:
            doc_list = do_aggregate(collection, projection, query, include_context)
        else:
            doc_list = do_find(collection, pagination, projection, query)

        return doc_list, total

    def apply_update(self, update_domain: UpdateDomain) -> int:
        client, db, collection = self._connect_to_db()

        query = update_domain.query
        data = update_domain.data
        loguru.logger.info(f"query={query}_data={data}")

        count = do_update(collection, query, data)
        return count

    def apply_update_many(self, update_domain: UpdateManyDomain) -> int:
        client, db, collection = self._connect_to_db()

        query = update_domain.query
        data = update_domain.data
        loguru.logger.info(f"query={query}_data={data}")
        count = do_update(collection, query, data, update_many=True)
        return count

    def apply_delete(self, domain: DeleteDomain):
        client, db, collection = self._connect_to_db()

        query = domain.query
        unique = domain.unique
        count = do_delete(collection, query, unique=unique, delete_many=False)
        return count

    def apply_delete_many(self, domain: DeleteManyDomain):
        client, db, collection = self._connect_to_db()

        query = domain.query
        count = do_delete(collection, query, unique=False, delete_many=True)
        return count
