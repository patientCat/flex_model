import json
from typing import Optional

import pymongo
from bson import json_util

from app.domain.database_ctx import context
from app.domain.lowcode_model.dsl.dsl_domain import FindDomain, CreateDomain, CreateManyDomain, FindManyDomain, \
    UpdateDomain, UpdateManyDomain


def remove_oid_and_date(obj):
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


def do_count(collection, query) -> int:
    total: int = collection.count(filter=query)
    return total


def do_update(collection, query, data, update_many=False) -> int:
    update = {
        "$set": data
    }
    result = collection.update_many(query, update)
    return result.modified_count


class MongoRepoService:
    def __init__(self, db_context: context):
        self.db_context: context.DbContext = db_context

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

        result = collection.insert_one(create_domain.data)
        return str(result.inserted_id)

    def apply_create_many(self, create_domain: CreateManyDomain) -> list:
        client, db, collection = self._connect_to_db()

        result = collection.insert_many(create_domain.datalist)

        id_list = []
        for _id in result.inserted_ids:
            id_list.append(str(_id))
        return id_list

    def apply_find(self, find_domain: FindDomain) -> (Optional[dict], Optional[int]):
        client, db, collection = self._connect_to_db()

        query = find_domain.where_node.to_dict()
        projection = find_domain.selector.select_dict
        pagination = find_domain.pagination
        doc_list = do_find(collection, pagination, projection, query)

        total = None
        if find_domain.with_count:
            total = do_count(collection, query)

        if len(doc_list) == 0:
            return None, total
        else:
            return doc_list[0], total

    def apply_find_many(self, find_many_domain: FindManyDomain) -> (Optional[list], Optional[int]):
        client, db, collection = self._connect_to_db()

        query = find_many_domain.where_node.to_dict()
        projection = find_many_domain.selector.select_dict
        pagination = find_many_domain.pagination
        doc_list = do_find(collection, pagination, projection, query)

        total = None
        if find_many_domain.with_count:
            total = do_count(collection, query)

        return doc_list, total

    def apply_update(self, update_domain: UpdateDomain) -> int:
        client, db, collection = self._connect_to_db()

        query = update_domain.query
        data = update_domain.data
        count = do_update(collection, query, data)
        return count

    def apply_update_many(self, update_domain: UpdateManyDomain) -> int:
        client, db, collection = self._connect_to_db()

        query = update_domain.query
        data = update_domain.data
        count = do_update(collection, query, data, update_many=True)
        return count
