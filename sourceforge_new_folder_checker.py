from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from datetime import datetime
import platform


def telegram_message():
    # options - in order to make headless search with Edge
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')

    # Edge web drivers can be found on https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    # it helps to choose the right architecture in order to get the driver correctly
    driver_path = "msedgedriver64.exe" if platform.machine().endswith("64") else "msedgedriver32.exe"

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # set the url that we will check for new folders
    target_url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/"

    # opens the web page
    driver.get(target_url)

    # getting the info from the first row in the table. Index 0 is table head, index 1 is folder, date, etc.
    table = driver.find_element("xpath", '//*[@id="files_list"]/tbody/tr[1]')

    # table.text returns string separated by new lines
    # splitting the string into list, because the 1st element (index 0)
    # #contains the last folder name and last date of modification
    full_info = table.text.split("\n")[0]

    # creating variables for the founded elements - folder, date (or hours) since last modification
    current_name = ""
    found_date = ""
    new_folder_found = False

    def check_date(folder_date_list, new_folder_checker):
        folder_name, date = folder_date_list

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
        current_name, found_date = full_info.split(" < ")
        new_folder_found = True
    else:
        current_name, found_date, new_folder_found = check_date(full_info.split(), new_folder_found)

    if new_folder_found:
        output = f"Modified folder found!\nName: {current_name}\nDate: {found_date}\n" \
                 f""f"Download link: {target_url + current_name}"
    else:
        output = f"Everything is the same as in {found_date}\n" \
                 f"Last created folder is {current_name}\nBetter luck next time!"

    return output


# if you just want to view the message without sending it to Telegram, just print the function:
# print(telegram_message())
