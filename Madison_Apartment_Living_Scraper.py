
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import re
import requests
import openrouteservice as ors
import csv
import os
# Config parser was renamed in Python 3
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

def newPage(driver):
    #this piece of code locates the buttons to change page so all pages can be scraped
    a_elements = driver.find_elements(By.CLASS_NAME, "page-link")
    
    #arr to store results
    arr2 = []
    
    #iterate through each of the pages
    for a in range(0,len(a_elements)):
        
        #page elements have to be continously scraped otherwise
        #a stale reference error will be thrown
        a_elements = driver.find_elements(By.CLASS_NAME, "page-link")
        
        #page is changed here
        driver.execute_script("arguments[0].click();", a_elements[a])
        arr2 = arr2 + individualApts(driver)
    
    return arr2
        
def individualApts(driver)  :
    
    #this code gets the html
    div_element = driver.find_element_by_id('searchResult')

    # get the HTML content of the div
    div_html = div_element.get_attribute('innerHTML')

    # parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(div_html, 'html.parser')
    arr1 = []
    # now you can use Beautiful Soup methods to navigate and search the div contents
    my_links = soup.find_all('a',href=True)
    
    #running the code headless
    options = Options()
    options.headless = True
    driver2 = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    for link in my_links:
            
            url = link['href'];
            if str(url)[0] == '/':
               
                driver2.get("https://www.madisonapartmentliving.com" + str(url) )
                soup2 = BeautifulSoup(driver2.page_source)
                
                #rent values
                rent_label = soup2.find( 'small', text="Monthly Rent")
                rent_value = rent_label.find_next('p', class_='m-0').text.strip()
                
                address = soup2.find(class_="showMap yesprint tempLinkColor").text
                
                #name of complex
                title = soup2.find('h1').text.strip()
                print(title)
                uw_distance = ''
                uw = soup2.find( 'h6', text="University of Wisconsin-Madison")
                try:
                    uw_distance = uw.find_next('p', class_='card-text card-dist').text.strip()
                except:
                    pass
                print(uw_distance)
              
                
                epic_distance = ''
                epic1 = soup2.find( 'div', text="Epic")
                try:
                    epic_distance = epic1.find_next('div', class_='col-2 col-md-2 text-secondary').text.strip()
                except:
                    pass
         
                arr1.append([title, address.encode('ascii', 'ignore').decode('ascii'),rent_value,epic_distance,uw_distance])
       
    driver2.close()
    return arr1

def accessMAL(no_beds, max_rent, baths_any,
                       bath_1, bath_2, bath_3, 
                       cats_allowed, dogs_allowed, 
                       short_term_lease, corporate,
                       furnished, brand_new, 
                       fitness_center, pool, 
                       in_unit_washer_dryer, 
                       laundry_facilities, 
                       off_street_parking, 
                       covered_parking,
                       utilities_included)  :
  
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get("https://www.madisonapartmentliving.com/search.j")
    #stores all the ids for the number of bedrooms
    bed_arr = ["btnb0","btnb1","btnb2","btnb3","btnb4","btnb5"]
   #max number of bedrooms is 5
    if no_beds >= 5:
        bedrooms_button = driver.find_element(By.ID, bed_arr[5])
        driver.execute_script("arguments[0].click();", bedrooms_button)
    else:
        counter = 0
        while counter <= no_beds:
            bedrooms_button = driver.find_element(By.ID, bed_arr[counter])
            counter = counter + 1;
            driver.execute_script("arguments[0].click();", bedrooms_button)
     
    #picks max rent from rent dropdwon
    dropdown = driver.find_element(By.ID, "navbarDropdown")
    dropdown.click()
    max_rent_dd = Select(driver.find_element(By.ID, "maxRentDD"))
    
    max_rent_dd.select_by_value(max_rent)
    
    #goes through the rest of the options
    
    if baths_any:
        baths_any_checkbox = driver.find_element(By.ID, "checkw0")
        driver.execute_script("arguments[0].click();", baths_any_checkbox)

    if bath_1:
        bath_1_checkbox = driver.find_element(By.ID, "checkw1")
        driver.execute_script("arguments[0].click();", bath_1_checkbox)

    if bath_2:
        bath_2_checkbox = driver.find_element(By.ID, "checkw2")
        driver.execute_script("arguments[0].click();", bath_2_checkbox)

    if bath_3:
        bath_3_checkbox = driver.find_element(By.ID, "checkw3")
        driver.execute_script("arguments[0].click();", bath_3_checkbox)

    if cats_allowed:
        cats_allowed_checkbox = driver.find_element(By.ID, "checkCats")
        driver.execute_script("arguments[0].click();", cats_allowed_checkbox)

    if dogs_allowed:
        dogs_allowed_checkbox = driver.find_element(By.ID, "checkDogs")
        driver.execute_script("arguments[0].click();", dogs_allowed_checkbox)

    if short_term_lease:
        short_term_lease_checkbox = driver.find_element(By.ID, "checkm1")
        driver.execute_script("arguments[0].click();", short_term_lease_checkbox)

    if corporate:
        corporate_checkbox = driver.find_element(By.ID, "checkm2")
        driver.execute_script("arguments[0].click();", corporate_checkbox)

    if furnished:
        furnished_checkbox = driver.find_element(By.ID, "checkm3")
        driver.execute_script("arguments[0].click();", furnished_checkbox)

    if brand_new:
        brand_new_checkbox = driver.find_element(By.ID, "checkm18")
        driver.execute_script("arguments[0].click();", brand_new_checkbox)

    if fitness_center:
        fitness_checkbox = driver.find_element(By.ID, "checkm6")
        driver.execute_script("arguments[0].click();", fitness_checkbox)
    if pool:
        swimming_pool = driver.find_element(By.ID, "checkm7")
        driver.execute_script("arguments[0].click();", swimming_pool)

    if in_unit_washer_dryer:
        washer_dryer = driver.find_element(By.ID, "checkm31")
        driver.execute_script("arguments[0].click();", washer_dryer)

    if laundry_facilities:
        laundry = driver.find_element(By.ID, "checkm55")
        driver.execute_script("arguments[0].click();", laundry)

    if off_street_parking:
        off_street = driver.find_element(By.ID, "checkm39")
        driver.execute_script("arguments[0].click();", off_street)

    if covered_parking:
        covered = driver.find_element(By.ID, "checkm38")
        driver.execute_script("arguments[0].click();", covered)

    if utilities_included:
        utilities = driver.find_element(By.ID, "checkm49")
        driver.execute_script("arguments[0].click();", utilities)
    
    #adds everything the the array
    arr = [["Name","Address", "Rent", "Distance to Epic", "Distance to UW Madison"]]
    arr = arr + newPage(driver)
    
    return arr

def round_to_nearest_100(number):
    number = int(number)
  
    if number < 500:
        return 500
    elif number > 5000:
        return 5000
    else:
        return str(round(number / 100) * 100)

def con_extraction():
    
    conf = configparser.ConfigParser()
    config_file = os.path.join(os.getcwd(), "config.ini")
    conf.read(config_file)
    no_beds = int(conf.get('all', 'beds'))
    max_rent = round_to_nearest_100(conf.get('all', 'max_rent'))
    baths_any = conf.getboolean('all', 'baths_any')
    bath_1 = conf.getboolean('all', '1bath')
    bath_2 = conf.getboolean('all', '2bath')
    bath_3 = conf.getboolean('all', '3bath')

    cats_allowed = conf.getboolean('all', 'cats_allowed')
    dogs_allowed = conf.getboolean('all', 'dogs_allowed')
    short_term_lease = conf.getboolean('all', 'short_term_lease')
    corporate = conf.getboolean('all', 'corporate')
    furnished = conf.getboolean('all', 'furnished')
    brand_new = conf.getboolean('all', 'brand_new')
    fitness_center = conf.getboolean('all', 'fitness_center')
    pool = conf.getboolean('all', 'pool')
    in_unit_washer_dryer = conf.getboolean('all', 'in_unit_washer/dryer')
    laundry_facilities = conf.getboolean('all', 'laundry_facilities')
    off_street_parking = conf.getboolean('all', 'off_street_parking')
    covered_parking = conf.getboolean('all', 'covered_parking')
    utilities_included = conf.getboolean('all', 'utilites_included')
    arr = accessMAL(no_beds, max_rent, baths_any,
                       bath_1, bath_2, bath_3, 
                       cats_allowed, dogs_allowed, 
                       short_term_lease, corporate,
                       furnished, brand_new, 
                       fitness_center, pool, 
                       in_unit_washer_dryer, 
                       laundry_facilities, 
                       off_street_parking, 
                       covered_parking,
                       utilities_included)  
    return arr
    
  
def main():
    con_extraction()
    arr = con_extraction()
    with open('madison_apartments1.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(arr)
main()



