from scraper import scrape_config_by_url


rom_folders = {}
def get_all_folders(url):
    # go to main folder and create soup
    soup = scrape_config_by_url(url)
    # get all subfolders
    element_list = soup.find_all('tr', class_='folder')
    # iterate through subfolders to get their subfolders
    for element in element_list[1:]:
        current_folder = element.find('a')
        current_soup = scrape_config_by_url("https://sourceforge.net" + current_folder['href'])
        current_element_list = current_soup.find_all('tr', class_='folder')
        for current_element in current_element_list[1:]:
            folder = current_element.find('a')
            rom_folders[folder.text.strip()] = "https://sourceforge.net" + folder['href']
    return rom_folders

print(get_all_folders("https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/").keys())
