# Contains all the errors for better handeling in the module

class UnexpectedDataGetAction(Exception):
    """Used when the data retrieval action is not what was expected. Generic for any kind of error that might
    occur when trying to retrieve data.

    Args:
        RentalCo (str): The name of the rental company that the error occured with.
        reason (str): The reason for the error.
    """
    
    def __init__(self, RentalCo, reason):
        self.message = "There was an error with retrieving the data for " + RentalCo + "::" + reason
        super().__init__(self.message)
        
class InvalidDataShapeReceived(Exception):
    """Used when the shape of the data that is inputted into a RentalCompany instance is not what is expected.
    More specifically, it checks for the columns of the inputted data. The expected number of columns is 
    specified in the _COLUMNS variable.

    Args:
        actual (int): The actual number of columns that was inputted.
    """
    
    def __init__(self, actual):
        
        _COLUMNS = 7
        
        self.message = "There was an error with the given data. Expected " + _COLUMNS + " colums, but got " + str(len(actual)) + " instead."
        super().__init__(self.message)