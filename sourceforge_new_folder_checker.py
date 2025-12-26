from datetime import datetime
from scraper import scrape_config_by_url

# BeautifulSoup instance that gets url and parser as arguments
# url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-WEEKLY-RELEASES/"
url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/HyperOS-STABLE-RELEASES/"
soup = scrape_config_by_url(url)

# getting the info directly from the html by id of the table
results = soup.find(id="files_list")
# getting all table rows with this class in order to get the folder name and last modification date (or hours)
folders = results.find_all('tr', class_="folder")
# this variable will contain the result of the first valid row
# (that isn't contain "Parent Folder" or other irrelevant information)
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

    # getting the difference in days (it gave something like "2 days, 14:05:28.657927", which is translated to
    # number with ".days" in the "if" statement)
    days_difference = datetime.now() - datetime(found_year, found_month, found_day)
    if days_difference.days < 4:
        new_folder_checker = True
        date = f"{found_year}-{found_month}-{found_day}"
    return folder_name, date, new_folder_checker


# checking if the folder is newly created ( last 24 hours )
if "<" in full_info:
    current_name, found_date = full_info[0], " ".join(full_info[1:5])
    new_folder_found = True
else:
    current_name, found_date, new_folder_found = check_date(full_info[0], full_info[1], new_folder_found)

if new_folder_found:
    output = f"Modified folder found!\nName: {current_name}\nDate: {found_date}\n" \
             f""f"Download link: {url + current_name}"
else:
    output = f"Everything is the same as in {found_date}\n" \
             f"Last created folder is {current_name}\nBetter luck next time!"

print(output)