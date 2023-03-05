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
    
    def dataSet(self, data: list) -> None:
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
  
    def newConnection(self, user: str, pw: str, server: str) -> None:
        """Creates a new connection to a mongoDB database using SCRAM and connection string.

        Args:
            user (str): mongoDB username
            pw (str): mongoDB password
            server (str): mongoDB server address
        """
        _clientURL = "mongodb+srv://" + user + ":" + pw + "@" + server + "/?retryWrites=true&w=majority"
        self.__client = pm.MongoClient(_clientURL)

    def connection(self) -> pm.MongoClient:
        """Returns the mongoDB client connection. Safety checks to makes sure there is a connection first.
        
        Returns:
            (pm.MongoClient): The mongoDB client connection.
        """
        
        if self.__client == None:
            raise Exception("Error:: _utils.DatabaseConnectionMongoDB tried to retrieve a connection but there is none.")
        
        return self.__client
    
    def setDatabase(self, db: str) -> None:
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
    
    def setCollection(self, collection: str) -> None:
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
    
    def newDatabase(self, db: str) -> None:
        """Creates a new database in the mongoDB server.
        
        Args:
            db (str): The name of the database to be created.
        """
        
        self.__database = self.__client[db]
    
    def newCollection(self, collection: str) -> None:
        """Creates a new collection in the mongoDB server.
        
        Args:
            collection (str): The name of the collection to be created.
        """
        
        self.__collection = self.__database[collection]
    