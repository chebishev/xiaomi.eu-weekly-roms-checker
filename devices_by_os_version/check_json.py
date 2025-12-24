import json
import sys
sys.path.append("../")

main_link = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/"
links_to_files = {
    "HyperOS 1.0.json": f"{main_link}HyperOS-STABLE-RELEASES/HyperOS1.0/",
    "HyperOS 2.0.json": f"{main_link}HyperOS-STABLE-RELEASES/HyperOS2.0/",
    "HyperOS 3.0.json": f"{main_link}HyperOS-STABLE-RELEASES/HyperOS3.0/",
    "MIUI 12.json": f"{main_link}MIUI-STABLE-RELEASES/MIUIv12/",
    "MIUI 13.json": f"{main_link}MIUI-STABLE-RELEASES/MIUIv13/",
    "MIUI 14.json": f"{main_link}MIUI-STABLE-RELEASES/MIUIv14/",

}

# this will be used from drowpdown menu, so there will be no mistakes
file_name = input("Enter OS version file name (e.g., HyperOS 3.0.json): ")
if file_name not in links_to_files:
    print("Unknown OS version file")
    sys.exit(1)
    
device_model = input("Enter device market name (e.g., Xiaomi 15): ")
with open(file_name, "r", encoding="utf-8") as f:
    data = json.load(f)

# be sure that the json is not a list, but a dict
if not isinstance(data, dict):
    print("JSON file format is incorrect")
    sys.exit(1)
chosen_model = data[device_model]["rom_name"]

from scraper import scrape_config_by_url as scrape

soup = scrape(links_to_files[file_name])
rows = soup.find_all("tr", class_="file")

for row in rows:
    a = row.find("a", href=True)
    if not a:
        continue
   
    name = a["href"]
    # skip the "Parent folder" row
    if name == "..":
        continue

    if chosen_model not in name:
        continue

    print(name)
    break
else:
    print("no such model found")
