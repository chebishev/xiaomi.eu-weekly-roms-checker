from scraper import scrape_config_by_url


def telegram_message() -> dict:
    telegram_message = {
        "title": "",
        "sourceforge": "", 
        # "androidfilehost": "",
        "image_url": "",
        "changelog": []
        }
    soup = scrape_config_by_url("https://xiaomi.eu/community/threads/hyperos-3-0-stable-release.76151/")
    telegram_message["title"] = soup.find('h1').find('span').text
    all_links = soup.find_all("a", href=True, class_="link link--external")
    for link in all_links:
        if "sourceforge.net" in link.text:
            telegram_message["sourceforge"] = link['href']
        # if "androidfilehost.com" in link.text:
        #     telegram_message["androidfilehost"] = link['href']
    post_images = soup.find_all("div", class_="bbImageWrapper")
    for image in post_images:
        current_url = image.find("img")['src']
        if ".png" in current_url:
            telegram_message["image_url"] = current_url
            break
    changelog = soup.find_all('div', class_="bbWrapper")
    for c in changelog:
        current_result = c.text.split(".")
        if current_result[0].startswith("CHANGELOG"):
            telegram_message["changelog"].append(current_result)
    return telegram_message

# for printing directly on the console
# print(telegram_message())
