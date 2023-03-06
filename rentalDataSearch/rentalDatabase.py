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
        super()._setDatabase(dataBase)
        self.__db = dataBase
        
    def setCompany(self, company: str) -> None:
        """Sets the collection to the company name. This is used to get the data for a specific company.
        If the collection in the database does not exist, it will create it.

        Args:
            company (str): The name of the company to get the data for.
        """
        try:
            super()._setCollection(company)
        except:
            print("DEBUG:: No existing collection for this company found. Creating new collection for " + company)
            super()._createCollection(company)
            super()._setCollection(company)  
    
    def insertListOfDataEntry(self, doc: list) -> None:
        """Inserts a new data entry into the database. No checks to the data are made before inserting it.
        If it is a list, it will insert all the documents in the list. Depending on the database it is connected to,
        it will also insert the data appropriately.

        Args:
            data (list): a list of dictionaries containing the data to be inserted.
            
        Raises:
            Exception: Will raise if the database is not rental-data or rental-history.
        """
        
        # Check what database we are connected to. Then for each entry,
        # try to retrieve an existing document in the db based on the 
        # address.
        if self.__db == "rental-data":
            for d in doc:
                eDoc = super()._getOneDocument({"address" : d["address"]})
                
                # If there is not an existing document, insert the new document.
                if eDoc == None:
                    super()._setOneDocument(d)
                
        elif self.__db == "rental-history":
            for d in doc:
                eDoc = super()._getOneDocument({"address" : d["address"]})
                
                # If there is not an existing document, insert the new document.
                # otherwise, update the existing document and reinsert into db.
                if eDoc == None:
                    super()._setOneDocument(d)
                else:
                    for date in d["history"]:
                        eDoc["history"][date] = d["history"][date]
                        
                    super()._updateOneDocument({"address" : eDoc["address"]}, {"$set" : {"history" : eDoc["history"]}})
        else:
            raise Exception("DEBUG:: Unknown database. Cannot insert data.")