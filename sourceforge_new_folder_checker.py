from selenium import webdriver
import time

# set location of our edge driver
edge_driver_path = "edgedriver_win64/msedgedriver.exe"
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
