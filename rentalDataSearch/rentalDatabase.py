import pymongo as pm
from ._utils import DatabaseConnectionMongoDB

class RentHistoryData(DatabaseConnectionMongoDB):
    """This class is used to grab rent history data from the database. It assumes that the database is a mongoDB.
    
    Args:
        see _utils.DatabaseConnectionMongoDB for args.
    
    """
    def __init__(self, user: str, pw: str, server: str) -> None:
        super().__init__(user, pw, server)