from datetime import datetime
import requests
from bs4 import BeautifulSoup


# from selenium import webdriver
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
#
#
# def get_driver():
#     # options - in order to make headless search with Edge
#     options = Options()
#     options.use_chromium = True
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument('--allow-running-insecure-content')
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--log-level=3')  # remove errors about "Error with Feature-Policy header
#
#     # get and install the newest, needed driver in .root/.wdm
#     service = EdgeService(EdgeChromiumDriverManager().install())
#
#     return webdriver.Edge(service=service, options=options)


def telegram_message():
    # driver = get_driver()
    #
    # # set the url that we will check for new folders target_url =
    # "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/"
    #
    # # opens the web page
    # driver.get(target_url)

    # getting the info from the first row in the table. Index 0 is table head, index 1 is folder, date, etc.
    # table = driver.find_element("xpath", '//*[@id="files_list"]/tbody/tr[1]')

    # table.text returns string separated by new lines
    # splitting the string into list, because the 1st element (index 0)
    # #contains the last folder name and last date of modification
    # full_info = table.text.split("\n")[0]

    # url needed for beautiful soup to do its magic:
    url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/"
    page = requests.get(url)

    # BeautifulSoup instance that gets url and parser as arguments
    soup = BeautifulSoup(page.content, "html.parser")
    # getting the info directly from the html by id of the table
    results = soup.find(id="files_list")
    # getting all table rows with this class in order to get the folder name and last modification date (or hours)
    folders = results.find_all('tr', class_="folder")
    # this variable will contain the result of the first valid row
    # (that isn't cointain "Parent Folder" or other irrelevant information)
    full_info = ""

    # getting all the rows, but we need only the first valid one since it is the folder that we are checking
    for folder in folders:
        if "Parent" in folder.text:
            continue
        full_info = folder.text.split()
        break

    # creating variables for the founded elements - folder, date (or hours) since last modification
    current_name = ""
    found_date = ""
    new_folder_found = False

    def check_date(folder_found, date_found, new_folder_checker):
        folder_name, date = folder_found, date_found

        # extracting year, month, day from found_date string
        found_year, found_month, found_day = [int(x) for x in date.split("-")]

        # getting the difference in days (it gaves something like "2 days, 14:05:28.657927", which is translated to
        # number with ".days" in the "if" statement)
        days_difference = datetime.now() - datetime(found_year, found_month, found_day)
        if days_difference.days < 4:
            new_folder_checker = True
            date = f"{found_year}-{found_month}-{found_day}"
        return folder_name, date, new_folder_checker

    # checking if the folder is newly created ( last 24 hours )
    if " < " in full_info:
        current_name, found_date = full_info[0], full_info[1]
        new_folder_found = True
    else:
        current_name, found_date, new_folder_found = check_date(full_info[0], full_info[1], new_folder_found)

    if new_folder_found:
        output = f"Modified folder found!\nName: {current_name}\nDate: {found_date}\n" \
                 f""f"Download link: {url + current_name}"
    else:
        output = f"Everything is the same as in {found_date}\n" \
                 f"Last created folder is {current_name}\nBetter luck next time!"

    return output


# if you just want to view the message without sending it to Telegram, just print the function:
print(telegram_message())
