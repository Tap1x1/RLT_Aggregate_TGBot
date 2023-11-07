from datetime import datetime
from database import Database
from config import DATABASE_NAME, DATABASE_URI, COLLECTION_NAME, START_DATE, END_DATE, GROUP_TYPE


def main():
    database = Database(DATABASE_NAME, COLLECTION_NAME, DATABASE_URI)

    start_date = datetime.fromisoformat(START_DATE)
    end_date = datetime.fromisoformat(END_DATE)

    result =  database.aggregate_data(start_date, end_date, GROUP_TYPE)
    print(result)

if __name__ == "__main__":
    main()