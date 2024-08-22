import requests

from scraper import scrape_config_by_url


def get_all_folders(url, rom_type):
    found_folders = {}
    soup = scrape_config_by_url(url)
    result = soup.find(class_="folders")
    folders = result.find_all("a")
    for folder in folders:
        current_folder = folder.text
        if rom_type == "weekly":
            if not current_folder[0].isdigit():
                continue
        found_folders[current_folder] = folder['href']
    return found_folders


main_url = "https://androidfilehost.com"
all_folders_url = "https://androidfilehost.com/?w=files&flid=18823"
stable_url = "https://androidfilehost.com/?w=files&flid=36337"

all_folders = {
    "weekly": get_all_folders(all_folders_url, "weekly"),
    "stable": get_all_folders(stable_url, "stable")
}
counter = 0
for folder_type, inner_folders in all_folders.items():
    for current_folder, url in inner_folders.items():
        new_url = main_url + url
        folder_soup = scrape_config_by_url(new_url)
        try:
            folder_results = folder_soup.find(class_="file-name")
            element = folder_results.find("a")
            # prints the result in format:
            # 20.1.15 -> xiaomi.eu_multi_MINote10_MICC9Pro_20.1.15_v11-9.zip - https://androidfilehost.com/?fid=4349826312261703062
            # print(f"{current_folder} -> {element.text} - {main_url+ element['href']}")
            counter += 1
        except Exception as e:
            print("### ERROR ###")
            print(e)
            print(f"{current_folder} -> {url}")


print(counter)
