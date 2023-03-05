import pymongo as pm
from ._utils import DatabaseConnectionMongoDB

class RentHistoryData(DatabaseConnectionMongoDB):
    """This class is used to grab rent history data from the database. It assumes that the database is a mongoDB.
    
    Args:
        see _utils.DatabaseConnectionMongoDB for args.
    
    """
    def __init__(self, user: str, pw: str, server: str, dataBase: str) -> None:
        """Creates the instance of the class connected to the rental-data database.

        Args:
            See _utils.DatabaseConnectionMongoDB for args.
        """
        super().__init__(user, pw, server)
        super().setDatabase(dataBase)
        
    def company(sef, company: str) -> None:
        """Sets the collection to the company name. This is used to get the data for a specific company.

        Args:
            company (str): The name of the company to get the data for.
        """
        super().setCollection(company)
    