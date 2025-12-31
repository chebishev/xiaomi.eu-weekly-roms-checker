from scraper import scrape_config_by_url as scrape
from urllib.parse import urljoin

def parse_folder(name):
    if name.startswith("HyperOS"):
        return "HyperOS", float(name.replace("HyperOS", ""))
    if name.startswith("MIUIv"):
        return "MIUI", int(name.replace("MIUIv", ""))
    return None, None


def get_subfolders(url):
    """
    Returns list of (folder_name, folder_url) tuples.
    Skips "Parent folder".
    """
    soup = scrape(url)

    rows = soup.find_all("tr", class_="folder")

    subfolders = []

    for row in rows:
        a = row.find("a", href=True)
        if not a:
            continue

        name = a.text.strip()

        # skip the "Parent folder" row
        if name.lower().startswith("parent"):
            continue

        folder_url = urljoin("https://sourceforge.net", a["href"])
        subfolders.append((name, folder_url))

    return subfolders


def crawl_all(url, result=None):
    """
    Recursively crawl all nested folders and return dict:
    { ROM_FAMILY: { "min": min_version, "max": max_version } }
    """
    if result is None:
        result = {}

    for name, suburl in get_subfolders(url):

        # Store this folder
        if name.endswith("RELEASES"):
            crawl_all(suburl, result)
            continue

        family, version = parse_folder(name)
        if family is None:
            crawl_all(suburl, result)
            continue

        if family not in result:
            result[family] = {"min": version, "max": version}
        else:
            result[family]["min"] = min(result[family]["min"], version)
            result[family]["max"] = max(result[family]["max"], version)

        crawl_all(suburl, result)

    return result

root_url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/"
print(crawl_all(root_url))