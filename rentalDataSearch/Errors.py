# Contains all the errors for better handeling in the module

class UnexpectedDataGetAction(Exception):
    
    def __init__(self, property, reason):
        self.message = "There was an error with retrieving the data for " + property + "::" + reason
        super().__init__(self.message)