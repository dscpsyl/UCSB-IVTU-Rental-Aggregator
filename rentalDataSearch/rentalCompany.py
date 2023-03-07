from .Errors import UnexpectedDataGetAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from table_ocr import extract_tables, extract_cells, ocr_image, ocr_to_csv
import os
from datetime import datetime
import shutil
from ._utils import RentalCompany
from bs4 import BeautifulSoup as bs
import requests
import re


# https://www.studioplazaapts.com/rates/
class StudioPlazaApts(RentalCompany):
    
    def updateData(self) -> None:
        """Overloads from baseclass
            
        """
        data = []
        
        soup = bs(requests.get("https://www.studioplazaapts.com/rates/").content, "html.parser")
        table = (soup.find_all("table", {"class": "rates"}))[0]
        e = table.find_all("tr")
        for i in range(1, len(e)):
            r = []
            r.append("StudioPlazaApts") # Rental Company
            r.append(e[i].find_all("td")[0].text) # Address
            r.append("-1") # Bed
            r.append("-1") # Bath
            r.append("-1") # Tenants
            r.append("".join(re.findall(r'\d+', e[i].find_all("td")[1].text))) # Rent
            r.append(datetime.now().strftime("%m/%d/%Y,%H:%M:%S")) #Date Scanned

            data.append(r)
        
        self.data = data
        super()._dataToDocFormat()

# https://www.deanbrunner.com/property-listings/
class DeanBrunner(RentalCompany):
    
    def updateData(self) -> None:
        """Overloads from baseclass 
        """
        
        # Grab the html of the page from the website and select the table
        _URL = "https://www.deanbrunner.com/property-listings/"
        soup = bs(requests.get(_URL).content, "html.parser")
        table = soup.find(id="property_list")
        
        # Select only the properties from the table and get the raw data
        p = table.select("[style='background-color:#FFF'], [style='background-color:#EDEDED']")
        propsRAW = []
        for h in p: # h is each row (aka one property)
            hData = []
            i = 0
            for l in h: # l is each cell in the row
                if i > 3: # we only want the first 4 cells with text
                    break

                if l.text == "" or l.text == " " or l.text == "\n": # if the cell is empty and used for formatting
                    continue
            
                hData.append(l.text)
                i += 1
            propsRAW.append(hData)

        # Format the data
        data = []
        for p in propsRAW: # [Address | Bed/Bath | Tenants | Rent]
            entry = []
            time = datetime.now().strftime("%m/%d/%Y,%H:%M:%S")
            # [Rental Company | Address | Bed | Bath | Tenants | Rent | Date Scanned]
            entry.append("Dean Brunner")
            entry.append(p[0])
            entry.append(p[1][0])
            entry.append(p[1][2])
            entry.append(p[2])
            entry.append(p[3])
            entry.append(time)
            
            data.append(entry)
        
        self.data = data
        super()._dataToDocFormat() 

# https://www.beachtownrentals.com/properties
class BeachTownRentals(RentalCompany):

    def updateData(self) -> None:
        """Overloads from baseclass
            
        """
        
        # Set up the driver
        _URL = "https://www.beachtownrentals.com/properties"
        options = Options()
        options.add_argument('--headless')
        
        # Get the page screenshot
        driver = webdriver.Chrome(options=options)
        driver.get(_URL)
        driver.execute_script("window.scrollTo('60%', document.body.scrollHeight)") 
        driver.execute_script("document.body.style.zoom='85%'")
        driver.save_screenshot("env/beachtownrentals.png")
        
        # Extract the csv from the screenshot
        imageTables = extract_tables.main(["env/beachtownrentals.png"])
        if len(imageTables) != 1:
            raise UnexpectedDataGetAction("Beach Town Rentals", "Unexpected number of tables extracted from screenshot.")
        cells = extract_cells.main(imageTables[0][1][0])
        ocr = [ocr_image.main(cell, None)for cell in cells]
        csv = ocr_to_csv.main(ocr)
        
        # Clean up the csv
        csvEntry = []
        for l in csv.splitlines():
            if len(l) > 7:
                csvEntry.append(l.split(","))
        
        # Format each entry in the csv
        time = datetime.now().strftime("%m/%d/%Y,%H:%M:%S")
        data = []
        for rental in csvEntry:
            if rental[3] == '-':
                rental[3] = "-1"
            data.append(["Beach Town Rentals", rental[0], rental[1], "-1", rental[2], rental[3], time])
        
        # Delete the computed files
        os.remove("env/beachtownrentals.png")
        shutil.rmtree("env/beachtownrentals")
        
        self.data = data
        super()._dataToDocFormat()        