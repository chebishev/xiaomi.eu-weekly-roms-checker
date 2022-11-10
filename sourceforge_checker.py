from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import pandas as pd

driver = webdriver.Edge("edgedriver_win64/msedgedriver.exe")

driver.get("https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/")
table_data = []
content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('table', attrs={'id': "files-list"}):
    table_data.append(a)

print(table_data)
