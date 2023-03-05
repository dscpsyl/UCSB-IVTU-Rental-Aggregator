# A sample main file for the rentalDataSearch package. Main program is still in development.
from rentalDataSearch import *

print("Getting data from Beach Town Rentals...")
btr = beachtownrentals.Beachtownrentals()
btr.dataUpdate
print(btr.dataGetPretty())
print("#"*100)