# Definitions that are used by the dataSearch module
from .Errors import InvalidDataShapeReceived
import pandas as pd
import pymongo as pm

class RentalCompany:
    """The base class for all rental companies. It is used to store the data of the rental companies and provide
    data functions to the user.
    
    """
    
    def __init__(self) -> None:
        """It is expected for the user to use RentalCompany.data to retrieve the raw data stored in the instance.
        The format of self.data has the following format:
                        [[Rental Company | Address | Bed | Bath | Tenants | Rent | Date Scanned]]
            where each list of the self.data list is an entry.
        """
        
        self.data = []
        self.__propertyData = []
        self.__propertyRentHistory = []
    
    def __repr__(self) -> str:
        """ Returns the raw data of the instance.
        
        returns:
            (list(list(str))): The raw data of the inputted data.

        """    
        return str(self.data)
    
    def __str__(self) -> str:
        """ Returns a formatted pandas dataframe of the inputted data to prettify the information.

        returns:
            (pandas.DataFrame): A formatted pandas dataframe of the inputted data.

        """    
        
        # Check to make sure the list is not empty
        if not self.data:
            return("Rental Company  Address  Bed  Bath  Tenants  Rent  Date Scanned")

        _i = ["-" for i in range(len(self.data))]
        _c = ["Rental Company", "Address", "Bed", "Bath", "Tenants", "Rent", "Date Scanned"]
        d = pd.DataFrame(self.data, columns=_c).set_index(pd.Index(_i))

        return str(d)
    
    def setData(self, data: list) -> None:
        """ Gives the user the ability to set the data of the instance. It will check that the data format has
        the correct shape and nothing else. USE WITH CAUTION.
        
        args:
            data (list(list(str))): The raw data of properties that needs to be stored.
            
        raises:
            InvalidDataReceived: Will raise if the data is not in the correct format.

        """    
        
        for r in data:
            if len(r) != 7:
                raise InvalidDataShapeReceived(r)
        
        self.data = data

    def _dataToDocFormat(self) -> None:
        """ Function that converts self.data and splits it into two lists with an entry for each property:
            - self.__propertyData: A list of documents that contain the property data.
            - self.__propertyRentHistory: A list of documents that contain the rent history data.
        """
        for r in self.data:
            _doc = {
                "address": r[1],
                "beds": r[2],
                "baths": r[3],
                "tenants": r[4],
            }
            self.__propertyData.append(_doc)
            
            _doc = {
                "address": r[1],
                "history" : {
                    r[6] : r[5]
                }
            }
            
            self.__propertyRentHistory.append(_doc)
    
    def getDBData(self) -> list:
        """Returns the data in the database format. It will return as propertyData, propertyRentHistory.

        Args:
            type (str): The type of data to return. Can be "propertyData" or "propertyRentHistory".

        Returns:
            list: the list containing the documents
        """
        return self.__propertyData, self.__propertyRentHistory
        
class DatabaseConnectionMongoDB:
    """This is the base class for all database connections. It provides basic functions for database connection, interaction,
    and extractions. It works only with a mongoDB and assumes you are using SCRAM auth with connection link connection method. It is 
    not meant to be used directly.
    """
    
    def __init__(self, user: str, pw: str, server: str) -> None:
        """Connects to a mongoDB database using SCRAM and connection string. It will store, for each instance the:
            - mongoDB client connection
            - mongoDB database
            - mongoDB collection
            

        Args:
            user (str): mongoDB username
            pw (str): mongoDB password
            server (str): mongoDB server address
        """
        _clientURL = "mongodb+srv://" + user + ":" + pw + "@" + server + "/?retryWrites=true&w=majority"
        self.__client = pm.MongoClient(_clientURL)
        self.__database = None
        self.__collection = None
  
    def _newConnection(self, user: str, pw: str, server: str) -> None:
        """Creates a new connection to a mongoDB database using SCRAM and connection string.

        Args:
            user (str): mongoDB username
            pw (str): mongoDB password
            server (str): mongoDB server address
        """
        _clientURL = "mongodb+srv://" + user + ":" + pw + "@" + server + "/?retryWrites=true&w=majority"
        self.__client = pm.MongoClient(_clientURL)
    
    def _setDatabase(self, db: str) -> None:
        """Sets the desired db of the class instance. Safety checks to make sure that the databse exists.
        
        Args:
            db (str): The name of the database to be used.
            
        Raises:
            Exception: Will raise if the requested database does not exist.
            
        """
        
        _availableDBs = self.__client.list_database_names()
        if db not in _availableDBs:
            raise Exception("Error:: _utils.DatabaseConnectionMongoDB tried to set the database to " + db + " but it does not exist. Please use DatabaseConnectionMongoDB.newDatabase to create a new databaase first.")
        
        self.__database = self.__client[db]
    
    def _databasesList(self) -> list:
        """Returns a list of all the databases in the mongoDB server.
        
        Returns:
            (list(str)): A list of all the databases in the mongoDB server.
        """
        
        return self.__client.list_database_names()
    
    def _listDatabases(self) -> list:
        """Returns a list of all the databases in the mongoDB server.
        
        Returns:
            (list(str)): A list of all the names of the databases in the mongoDB server.
        """
        
        return self.__client.list_database_names()
        
    def _setCollection(self, collection: str) -> None:
        """Sets the desired collection of the class instance. Safety checks to make sure that the collection exists.
        
        Args:
            collection (str): The name of the collection to be used.
        
        Raises:
            Exception: Will raise if the requested collection does not exist.
        """
        
        _availableCollections = self.__database.list_collection_names()
        if collection not in _availableCollections:
            raise Exception("Error:: _utils.DatabaseConnectionMongoDB tried to set the collection to " + collection + " but it does not exist. Please use DatabaseConnectionMongoDB.newCollection to create a new collection first.")
        
        self.__collection = self.__database[collection]
    
    def _listCollections(self) -> list:
        """Returns a list of all the collections in the mongoDB server.
        
        Returns:
            (list(str)): A list of all the names of the collections in the mongoDB server.
        """
        
        return self.__database.list_collection_names()
    
    def _createCollection(self, collection: str) -> None:
        """Creates a new collection in the mongoDB server. Collection is not created until data is given.
        Thus, we will add data to it and then delete it.
        
        Args:
            collection (str): The name of the collection to be created.
        """
        
        self.__collection = self.__database[collection]
        self.__collection.insert_one({"_id": 0, "data": "data"})
        self.__collection.delete_one({"_id": 0})
        
    def _getCollection(self) -> pm.collection:
        """Returns the collection of the class instance.
        
        Returns:
            (pymongo.collection): The collection of the class instance.
        """
        
        return self.__collection
    
    def _listDocuments(self) -> list:
        """Returns a list of all the documents in the collection.
        
        Returns:
            (list(dict)): A list of all the documents in the collection.
        """
        
        return list(self.__collection.find())
    
    def _getOneDocument(self, search: dict) -> dict | None:
        """Returns a document from the collection based on a search query.
        
        Args:
            search (dict): The search query to find the document.
            
        Returns:
            (dict): The document from the collection. Will return None if no document is found.
        """
        
        return self.__collection.find_one(search)
    
    def _getMatchingDocuments(self, search: dict) -> list | None:
        """Returns a list of documents from the collection based on a search query.
        
        Args:
            search (dict): The search query to find the documents.
            
        Returns:
            (list(dict)): The documents from the collection. Will return None if no documents are found.
        """
        
        return list(self.__collection.find(search))
    
    def _setOneDocument(self, document: dict) -> None:
        """Sets a single document in the collection.
        
        Args:
            document (dict): The document to be set.
        """
        
        self.__collection.insert_one(document)
        
    def _replaceOneDocument(self, search: dict, update: dict) -> None:
        """Replaces a single document in the collection.
        
        Args:
            search (dict): The search query to find the document.
            update (dict): The update query to update the document.
            
        Raises:
            Exception: Will raise if the update query does not update exactly one document.
        """
        
        self.__collection.find_one_and_replace(search, update)
        
    def _updateOneDocument(self, search: dict, update: dict) -> None:
        """Updates a single document in the collection.
        
        Args:
            search (dict): The search query to find the document.
            update (dict): The update query to update the document.
            
        Raises:
            Exception: Will raise if the update query does not update exactly one document.
        """
        
        self.__collection.find_one_and_update(search, update)