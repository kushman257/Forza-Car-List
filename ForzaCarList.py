from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict


# The purpose of this function is to compile a list of manufacturers in Forza
# @input: string variable which holds the link of all manufacturers in Forza
#    > should be 'https://forza.fandom.com/wiki/Category:Manufacturers'
# @output: an array full of manufacturers in the game
def getListOfManufacturers(link):
    # Sends a GET request to the provided URL and stores the response in the 'page' variable
    page = requests.get(link)

    # Parses the retrieved HTML content from the page using BeautifulSoup
    # The 'html.parser' argument specifies that we're dealing with an HTML document
    soup = BeautifulSoup(page.content, 'html.parser')

    # Searches for a specific <div> element with the class 'category-page__members'
    # This <div> is assumed to contain a list of manufacturers
    list_items = soup.find('div', class_='category-page__members') 

    arr = []

    # Check if the 'list_items' was found (i.e., the <div> exists on the page)
    if list_items:
        # Finds all <li> (list item) elements within the <div>, assuming each manufacturer is in a list format
        list_items = list_items.find_all('li')

        # Loop through each <li> element
        for item in list_items:
            # Extracts the text content of each list item and strips any leading/trailing whitespace
            # The manufacturer name is stored in the text of the <li> element
            element = (item.text).strip()

            # Rename Briggs Automotive to BAC
            if element == 'Briggs Automotive Company':
                element  = 'BAC'

            # Drop '(manufacturer) from Lego Speed Champions
            if element ==  'LEGO Speed Champions (manufacturer)':
                element = 'LEGO Speed Champions'

            # There's a mistake in the page where 'Category:Manufacturers By Origin' is listed as a manufacturer
            # Dumps that value and any other unnecessary value.
            if element != 'Category:Manufacturers By Origin':
                    arr.append(element)
            
    return arr


# The purpose of the function is to strip data from the Forza website for all car models
# @input: links -> an array that holds all the links it should comb over
# @output: an array that has all the car models stored in it
def getListOfCars(link):

    cars = []

    for url in links:
        # Sends a GET request to the URL to retrieve the web page content
        page = requests.get(url)
        
        # Parses the retrieved page content using BeautifulSoup and creates a BeautifulSoup object
        # The 'html.parser' argument specifies that we are parsing an HTML document
        parsed_page = BeautifulSoup(page.content, 'html.parser')
        
        # Selects all table rows (<tr>) that are inside a table body (<tbody>)
        # This assumes that the car data is stored within rows of a table on the webpage
        table_rows = parsed_page.select('tbody tr')
        
        # Loop through each row found in the table body
        for row in table_rows:
            # Select the specific elements inside the row that match 'td div a' (anchors within divs inside table cells)
            # It is assumed that the car data is stored in these anchor tags
            data = row.select('td:first-child div a')

            # If we found any matching data within the row
            if data:
                try:
                    # Extracts the text from the first anchor tag and combines it with the text of its next sibling element (if present)
                    # This concatenation assumes that car details might be split across elements
                    car = data[0].text + ' ' + data[0].next_sibling.strip()
                except AttributeError:
                    # If an AttributeError occurs (likely because the next_sibling doesn't exist or is of an unexpected type),
                    # print an error message for debugging purposes
                    print("Throwing attribute error. Idk why...")

                if car not in cars:
                    cars.append(car)

    return cars


if __name__ == '__main__':
    link_for_manufacturers = 'https://forza.fandom.com/wiki/Category:Manufacturers'
    links = ["https://forza.fandom.com/wiki/Forza_Horizon_3/Cars",
            "https://forza.fandom.com/wiki/Forza_Horizon_4/Cars",
            "https://forza.fandom.com/wiki/Forza_Horizon_5/Cars"]

    manufacturers = getListOfManufacturers(link_for_manufacturers)

    models = getListOfCars(links)

    manufacturers.sort()

    # Keep doing this until the models array is empty
    while models:
    
        # Pick a manufacturer from the list of manufacturers
        for manufacturer in manufacturers:

            index = 0
            
            temp_arr = []

            while index < len(models):
                model = models[index]

                if model.startswith(manufacturer):
                    temp_arr.append(model)
                    models.pop(index)   
                    # Do not decrement index, as the next element shifts into the current index
                else:
                    index += 1
                # After picking out all the models, sort it by year (newer to older).
                    
        print( 'New Section\n\n')   
    # Append it to an excel file. 
    # Before heading to the next manufacturer, clear the temp array. 
    pass