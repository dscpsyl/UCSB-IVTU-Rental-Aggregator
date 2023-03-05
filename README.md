# UCSB - AS - IVTU - 2023 

Data aggregator for IV / Goleta / Santa Barbara / UCSB (CA, USA) rentals from major rental sites.
The only problem is that some method of aggregation is not completely fool-proof. If an upate
to a website is made, the aggregator might need to be updated.

## Database

The data is stored in a mongoDB database that is persistent and can only be accessed by this 
application with the correct credentials. The data can be requested by the application and
sent via a history class. Currently, it uses [MongoDB Atlas](https://cloud.mongodb.com/v2/) for development.

The database is structued such that each company has its own collection. Each document in the collection is 
a seperate address with the following structure:

```json
{
    "adddress" : "123 Main St",
    "beds" :  "2",
    "baths" : "2",
    "tenants" : "4",
    "rent" : ["1000", "1500.87"],
    "date" : ["12-23-1997", "01-03-2018"]
}
```

## Current Sites

Currently the following sites are in development:
* [Beach Town Rentals](https://www.beachtownrentals.com/)
