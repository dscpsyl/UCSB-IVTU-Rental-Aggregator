# Definitions that are used by the dataSearch module
import pandas as pd

class RentalCompany:
    def __init__(self) -> None:
        self.data = []
        pass
    
    def dataSet(self, data: list) -> None:
        """ Gives the user the ability to set the data of the instance. THIS FUNCTION DOES NOT
        CHECK FOR THE CORRECT DATA FORMAT. USE WITH CAUTION.
        
        args:
            data (list(list(str))): The raw data of properties that needs to be stored.

        """    
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