# UCSB - AS - IVTU - 2023 

Data aggregator for IV / Goleta / Santa Barbara / UCSB (CA, USA) rentals from major rental sites.
The only problem is that some method of aggregation is not completely fool-proof. If an upate
to a website is made, the aggregator might need to be updated.

## Database

The data is stored in a mongoDB database that is persistent and can only be accessed by this 
application with the correct credentials. The data can be requested by the application and
sent via a history class. Currently, it uses [MongoDB Atlas](https://cloud.mongodb.com/v2/) for development.

In the cluser, each database has a part of the full information on the specific property. The following databases 
are in the cluser are:
* rental-data : Contains the data infromation for each address
* rental-history : Contains specifically the rent history for each address

For each database, the collections are identified by the rental company name. This will monst likely be changed to a hash
for better "performance". Each document in the collection is a seperate address with the following structure:

```json
//rental-data
{
    "adddress" : "123 Main St",
    "beds" :  "2",
    "baths" : "2",
    "tenants" : "4",
}
```

```json
//rental-history
{
    "adddress" : "123 Main St",
    "history" : {
        //date : price
        "12/20/05" : "1050",
        "01/28/19" : "2400.78",
        //...
    }
}
```

If a certain field is not found in the aggregation, it will be set to a string of -1. This is to make it easier to
parse the data later on.

For security, any changes to the DB structure will be made outside of the program and the program itself will never be given 
the option to change the structure of the DB. It can only read the structure and write documents, and create clusters to the DB.

## Current Sites

Currently the following sites are in development:
* [Beach Town Rentals](https://www.beachtownrentals.com/)
* [Dean Brunner](https://www.deanbrunner.com/)
* [Studio Plaza Apartments](https://www.studioplazaapts.com/)

## Future Sites

The following sites are planned to be added in the future:
* [Sequioa Property Management](https://sequoiapropertiesonline.com/)
* [Gallagher Property Management](https://www.gpmproperties.com/)
* [Isla Vista Living](http://www.islavistaliving.com/index.html)
* [Embarcardero Company](https://www.embarcaderorentals.com/index.html)
* [Bartlein & Company](https://www.bartlein.com/)
* [Breakpoint & Coronado](https://www.breakpointeandcoronado.com/)
* [St George Associates](https://www.stgeorgeassociates.com/)
* [Eckert Investments](https://www.centralcoastrentals.com/)
* [Essex Apartment Homes](https://www.essexapartmenthomes.com/)
* [Harwin & Company](https://www.harwincosb.com/)
* [Icon Appartments](https://www.iconapts.com/)
* [IV Properties](https://www.ivproperties.com/)
* [Jeff Allen Properties](https://www.jeffallenproperties.com/)
* [KAMAP Property Managements](https://www.kamap.net/)
* [Meridian Group](https://meridiangrouprem.com/)
* [Sandpiper](http://www.sandpiperpropertymanagement.com/index.php)
* [SFM Vista Del Mar](https://www.sfmvdm.com/welcome/)
* [Shoreline Properties](https://www.sbrealty.com/)
* [Sierra Property Group](https://sierrapropsb.com/)
* [Spectrum Realty](https://www.spectrumrealty.com/)
* [Town & Country](https://www.townncountry-realty.com/)
* [Plaza Lofts IV](http://www.plazaloftsiv.com/)
* [Vista Del Capitan](http://www.vistadelcapitan.com/wordpress/)
* [Wolfe & Associates](https://www.rlwa.com/)
* [DMH Properties](https://www.dmhproperties.net/)