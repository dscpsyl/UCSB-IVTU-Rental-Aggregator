# A sample main file for the rentalDataSearch package. Main program is still in development.
from rentalDataSearch import *
import json as js

print("Creating new DB connection...")
settings = js.loads(open('env/cred.json').read())
rDataDB = rentalDatabase.RentHistoryData(settings["mongoDBUser"], settings["mongoDBPassword"], settings["mongoDBHost"], "rental-data")
rHistoryDB = rentalDatabase.RentHistoryData(settings["mongoDBUser"], settings["mongoDBPassword"], settings["mongoDBHost"], "rental-history")

#####################~[Beach Town Rentals]~#####################
print("Getting data from Beach Town Rentals...")
btr = rentalCompany.BeachTownRentals()
btr.updateData()
print("#"*100)
print(btr)
print("#"*100)

input(f"Please validate the data for formatting. If something does not look right, ABORT, FIX, and then rerun. Press enter to continue...")

print("Setting data for Beach Town Rentals...")
rentalPropData, rentalRentHist = btr.getDBData()
rDataDB.setCompany("BeachTownRentals")
rHistoryDB.setCompany("BeachTownRentals")
rDataDB.insertListOfDataEntry(rentalPropData)
rHistoryDB.insertListOfDataEntry(rentalRentHist)

#####################~[Dean Brunner]~#####################
print("Getting data from Dean Brunner...")
db = rentalCompany.DeanBrunner()
db.updateData()
print("#"*100)
print(db)
print("#"*100)

input(f"Please validate the data for formatting. If something does not look right, ABORT, FIX, and then rerun. Press enter to continue...")

print("Setting data for Dean Brunner...")
rentalPropData, rentalRentHist = db.getDBData()
rDataDB.setCompany("DeanBrunner")
rHistoryDB.setCompany("DeanBrunner")
rDataDB.insertListOfDataEntry(rentalPropData)
rHistoryDB.insertListOfDataEntry(rentalRentHist)

#####################~[Studio Plaza Apartments]~#####################
print("Getting data from Studio Plaza Apartments...")
spa = rentalCompany.StudioPlazaApts()
spa.updateData()
print("#"*100)
print(spa)
print("#"*100)

input(f"Please validate the data for formatting. If something does not look right, ABORT, FIX, and then rerun. Press enter to continue...")

print("Setting data for Studio Plaza Apartments...")
rentalPropData, rentalRentHist = spa.getDBData()
rDataDB.setCompany("StudioPlazaApts")
rHistoryDB.setCompany("StudioPlazaApts")
rDataDB.insertListOfDataEntry(rentalPropData)
rHistoryDB.insertListOfDataEntry(rentalRentHist)