print("Accessing timetable site...")
## Selenium Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options

## Setting up Firefox driver
options = Options() 
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options)

## Setting up csv files
import csv
# bookings file
bookings_file = open('data/room_bookings.csv', 'w+', newline='')
b_fieldnames = ['Room','Type','Day','Start','End','Weeks']
writer1 = csv.DictWriter(bookings_file,fieldnames=b_fieldnames)
writer1.writeheader()
# details file
details_file = open('data/room_details.csv', 'w+', newline='')
d_fieldnames = ['Room Code','Building','Floor','Room Number','Room Type']
writer2 = csv.DictWriter(details_file,fieldnames=d_fieldnames)
writer2.writeheader()

print("Scraping Rooms...")
## Scraping Rooms
# accessing Timetable site
driver.get("https://cts.strath.ac.uk/Scientia/live2425sws/default.aspx")
driver.find_element(By.ID, "LinkBtn_locations").click()
# parsing HTML
from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
rooms_list = soup.find("select", {"id": "dlObject"})
room = rooms_list.find_next("option")

### room loop
while True:
    if "&" in str(room): # if two rooms comined skip
        room = room.find_next("option")
    elif "<option selected=" in str(room): # if no more rooms break
        break
    else:
        ## Extracting room details from string
        room_string = str(room.get_text())
        # room number
        i = room_string.find("-")
        room_code = room_string[:i-1]
        # building
        j = i
        i = room_string.find("/",j+3)
        building = room_string[j+2:i-1]
        # floor
        j = i
        i = room_string.find("/",j+3)
        floor = room_string[j+2:i-1]
        # room number
        j = i
        i = room_string.find("/",j+3)
        room_number = room_string[j+2:i-1]
        # room type
        room_type = room_string[i+2:]
            # check if room number is present
        if not any(c.isnumeric() for c in room_number[:3]):
            room_type = room_string[j+2:]
            room_number = "NaN"        
        # write to csv
        writer2.writerow({'Room Code':room_code,'Building':building,'Floor':floor,'Room Number':room_number,'Room Type':room_type})
        
        ## Parsing room bookings from timetable
        # accessing Timetable site
        driver.get("https://cts.strath.ac.uk/Scientia/live2425sws/default.aspx")
        driver.find_element(By.ID, "LinkBtn_locations").click()
        try: # when room_string doesnt contain problematic characters
            # search for room
            input = driver.find_element(By.ID, "tWildcard")
            input.clear()  # Clear field
            input.send_keys(room_code)
            driver.find_element(By.ID, "bWildcard").click()
            # select room
            driver.find_element(By.XPATH, "//option[contains(text(),'"+room_string+"')]").click()
        except: # when room_string does contain problematic characters
            # search for room
            input = driver.find_element(By.ID, "tWildcard")
            input.clear()  # Clear field
            input.send_keys(room_string[:room_string.find("/")])
            driver.find_element(By.ID, "bWildcard").click()
            # select room            
            driver.find_element(By.XPATH, "//option[contains(text(),'"+room_string[:room_string.find("/")]+"')]").click()
        # select all weeks
        # driver.find_element(By.XPATH, "//option[contains(text(),'This Week')]").click()
        # select all day
        select = Select(driver.find_element(By.ID, "dlPeriod"))
        select.select_by_visible_text("All Day (08:00 - 22:00)")
        # select list format
        select = Select(driver.find_element(By.ID, "dlType"))
        select.select_by_visible_text("List (Ordered by Day / Time)")
        # view timetable
        driver.find_element(By.ID, "bGetTimetable").click()

        ### timetable row loop
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="spreadsheet")
        if table == None:
            print("Error with timetable page, could not complete action")
            break
        else:
            print("Scraping bookings for room "+room_code+"...")
            row = table.find_next("tr")
        while True:
            # scraping room timetable
            if room_code in str(row):
                type = row.find_next("td").find_next("td").find_next("td")
                day = type.find_next("td").find_next("td")
                start_time = day.find_next("td")
                end_time = start_time.find_next("td")
                weeks = end_time.find_next("td")
                # write to csv
                writer1.writerow({'Room':room_code,'Type':type.get_text(),'Day':day.get_text(),'Start':start_time.get_text(),'End':end_time.get_text(),'Weeks':weeks.get_text()})
                # next row in timetable
                row = row.find_next("tr")
            elif "Back To Selection" in str(row):
                break
            else:
                row = row.find_next("tr")

        # next room
        room = room.find_next("option")
