# https://www.beachtownrentals.com/properties

from .Errors import UnexpectedDataGetAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from table_ocr import extract_tables, extract_cells, ocr_image, ocr_to_csv
import os
from datetime import datetime
import shutil
from ._utils import RentalCompany


class Beachtownrentals(RentalCompany):

    def dataUpdate(self) -> None:
        """Updates the data from the webpage. It uses the webpage screenshot and OCR. This requires an internet connection and may not 
        always work due to the nature of OCR.

        Raises:
            UnexpectedDataGetAction: Will raise if OCR somehow extracts more than one table from the screenshot.
            
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
        