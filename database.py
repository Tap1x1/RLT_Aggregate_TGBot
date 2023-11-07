import logging
from pymongo import MongoClient

class Database:
    def __init__(self, database_name, collection_name, database_uri):
        self._client = MongoClient(database_uri)
        self._db = self._client[database_name]
        self._collection = self._db[collection_name]

    def aggregate_data(self, start_date: str, end_date: str, group_type: str) -> dict:

        def get_grouping(group_type: str) -> dict:
            grouping = {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '',
                            'date': '$dt'
                        }
                    },
                    'sum': {'$sum': '$value'}
                }
            }

            if group_type == "hour":
                grouping['$group']['_id']['$dateToString']['format'] = "%Y-%m-%dT%H:00:00"

            elif group_type == "day":
                grouping['$group']['_id']['$dateToString']['format'] = "%Y-%m-%dT00:00:00"

            elif group_type == "month":
                grouping['$group']['_id']['$dateToString']['format'] = "%Y-%m-01T00:00:00"

            else:
                logging.warning(f"unknown grouping: {group_type}, will group by `month` by default")
                grouping['$group']['_id']['$dateToString']['format'] = "%Y-%m-01T00:00:00"

            return grouping