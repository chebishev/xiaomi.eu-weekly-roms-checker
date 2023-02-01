from selenium import webdriver
from datetime import datetime
import time

# set location of our edge driver (you can get it from here:
# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
edge_driver_path = "msedgedriver.exe"
driver = webdriver.Edge(edge_driver_path)

# set the url that we will check for new folders
target_url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/"

# opens the web page
driver.get(target_url)

# wait x seconds before searching for the consent button
time.sleep(3)

# locate and click the "do not accept" button
consent_button = driver.find_element_by_xpath('//*[@id="cmpwelcomebtnno"]/a')
consent_button.click()

# getting all the info from the table
table = driver.find_elements_by_xpath('//*[@id="files_list"]')

full_info = ""
for items in table:
    full_info = items.text

# splitting the string into list, because the 6th element (index 5)
# #contains the last folder name and last date of modification
full_info = full_info.split("\n")
current_name, found_date = full_info[5].split()

# extracting year, month, day from found_date string
found_year, found_month, found_day = [int(x) for x in found_date.split("-")]

# getting the difference in days
# (it gaves something like "2 days, 14:05:28.657927", which is translated to number with ".days" in the "if" statement)
days_difference = datetime.now() - datetime(found_year, found_month, found_day)

if days_difference.days < 4:
    print(f"Modified folder found!\nName: {current_name}\nDate: {found_day}.{found_month}.{found_year}")
    print(f'Download link: {target_url+current_name}')
else:
    print(f"Everything is the same as in {found_date}\nLast created folder is {current_name}\nBetter luck next time!")