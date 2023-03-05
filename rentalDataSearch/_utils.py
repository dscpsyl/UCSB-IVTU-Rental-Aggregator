# Definitions that are used by the dataSearch module
from .Errors import InvalidDataShapeReceived
import pandas as pd
import pymongo as pm

class RentalCompany:
    """The base class for all rental companies. It is used to store the data of the rental companies and provide
    data functions to the user.
    """
    
    def __init__(self) -> None:
        self.data = []
        pass
    
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
    
    def dataGetRaw(self) -> list:
        """ Returns the raw data of the instance.
        
        returns:
            (list(list(str))): The raw data of the inputted data.

        """    
        return self.data
    
    def dataGetPretty(self) -> pd.DataFrame:
        """ Returns a formatted pandas dataframe of the inputted data.

        returns:
            (pandas.DataFrame): A formatted pandas dataframe of the inputted data.

        """    

        _i = ["-" for i in range(7)]
        _c = ["Rental Company", "Address", "Bed", "Bath", "Tenants", "Rent", "Date Scanned"]
        d = pd.DataFrame(self.data, columns=_c).set_index(pd.Index(_i))

        return d

class DatabaseConnectionMongoDB:
    """This is the base class for all database connections. It provides basic functions for database connection, interaction,
    and extractions. It works only with a mongoDB and assumes you are using SCRAM auth with connection link connection method. It is 
    not meant to be used directly.
    """
    
    def __init__(self, user: str, pw: str, server: str) -> None:
        """Connects to a mongoDB database using SCRAM and connection string.

        Args:
            user (str): mongoDB username
            pw (str): mongoDB password
            server (str): mongoDB server address
        """
        _clientURL = "mongodb+srv://" + user + ":" + pw + "@" + server + "/?retryWrites=true&w=majority"
        self.client = pm.MongoClient(_clientURL)
    

    def connection(self) -> pm.MongoClient:
        """Returns the mongoDB client connection.
        
        Returns:
            (pm.MongoClient): The mongoDB client connection.
        """
        return self.client
    
    
    
    