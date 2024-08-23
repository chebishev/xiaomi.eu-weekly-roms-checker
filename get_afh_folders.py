from scraper import scrape_config_by_url
from all_afh_folders import androidfilehost_xiaomieu_folders


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

# all_folders = {
#     "weekly": get_all_folders(all_folders_url, "weekly"),
#     "stable": get_all_folders(stable_url, "stable")
# }
all_afh_folders = androidfilehost_xiaomieu_folders
final_dict = {}
failed_links = []
for folder_type, inner_folders in all_afh_folders.items():
    for current_folder, url in inner_folders.items():
        if current_folder not in final_dict:
            final_dict[current_folder] = []
        new_url = main_url + url
        try:
            folder_soup = scrape_config_by_url(new_url)
            folder_results = folder_soup.find_all(class_="file")
            for element in folder_results:
                current_element = element.find("a")
                # # prints the result in format:
                # # 20.1.15 -> xiaomi.eu_multi_MINote10_MICC9Pro_20.1.15_v11-9.zip - https://androidfilehost.com/?fid=4349826312261703062
                final_dict[current_folder].append(current_element.text)
                final_dict[current_folder].append(current_element['href'])
        except Exception as e:
            print(f"{current_folder} - {url} - {e}")
            failed_links.append(new_url)

print(final_dict)
print(failed_links)
