from pymongo import MongoClient

class Database:
    def __init__(self, database_name, collection_name, database_uri):
        self._client = MongoClient(database_uri)
        self._db = self._client[database_name]
        self._collection = self._db[collection_name]

    def aggregate_data(self, start_date: str, end_date: str, group_type: str) -> dict:

        def get_grouping(group_type: str) -> dict:
            pass