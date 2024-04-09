import json
from typing import Optional

import pymongo
from bson import json_util

from app.service.db_luster import context
from app.service.model_domain.dsl.create_domain import CreateDomain, CreateManyDomain
from app.service.model_domain.dsl.find_domain import FindDomain


class CreateRepoService:
    def __init__(self, db_context: context.DbContext):
        self.db_context: context.DbContext = db_context

    def _connect_to_db(self):
        # 连接到MongoDB服务器
        client = self.db_context.create_client()

        # 选择一个数据库
        db = client[self.db_context.database_name()]

        # 选择一个集合(类似于表)
        collection = db[self.db_context.col_name()]

        return client, db, collection

    def apply(self, create_domain: CreateDomain) -> str:
        client, db, collection = self._connect_to_db()

        result = collection.insert_one(create_domain.data)
        return str(result.inserted_id)

    def apply_many(self, create_domain: CreateManyDomain) -> list:
        client, db, collection = self._connect_to_db()

        result = collection.insert_many(create_domain.datalist)

        id_list = []
        for _id in result.inserted_ids:
            id_list.append(str(_id))
        return id_list


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


class FindRepoService:
    def __init__(self, db_context: context, find_domain: FindDomain):
        self.db_context: context.DbContext = db_context
        self.find_domain: FindDomain = find_domain

    def _connect_to_db(self):
        # 连接到MongoDB服务器
        client = self.db_context.create_client()

        # 选择一个数据库
        db = client[self.db_context.database_name()]

        # 选择一个集合(类似于表)
        collection = db[self.db_context.col_name()]

        return client, db, collection

    def apply(self) -> Optional[dict]:
        client, db, collection = self._connect_to_db()

        query = self.find_domain.where_node.to_dict()
        projection = self.find_domain.selector.select_dict
        pagination = self.find_domain.pagination
        doc_list = do_find(collection, pagination, projection, query)

        if len(doc_list) == 0:
            return None
        else:
            return doc_list[0]
