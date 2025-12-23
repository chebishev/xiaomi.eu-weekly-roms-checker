import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

IMAGE_URLS = {
    # "MIUI 12": "https://provider.xiaomi.eu/img/devices_stable_v12_21121101.png",
    # "MIUI 13": "https://provider.xiaomi.eu/img/devices_stable_v13_23040300.png",
    # "MIUI 14": "https://provider.xiaomi.eu/img/devices_stable_v14_24011214.png",
    # "HyperOS 1.0": "https://provider.xiaomi.eu/img/devices_stable_os1_24122514.png",
    # "HyperOS 2.0": "https://provider.xiaomi.eu/img/devices_stable_os2_25070816.png",
    # "HyperOS 3.0": "https://provider.xiaomi.eu/img/devices_stable_os3_25121019.png",
    }


def extract_from_image(url):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "Extract ONLY the first 3 columns as structured JSON.\n"
                        "Columns: codename, market_names, rom_name.\n"
                        "Use market_names as key, because it is unique.\n"
                        "If rom_name is empty, fill it with \"TO_BE_FILLED_MANUALLY\"\n"
                        "Output JSON array only—no explanations."
                    )},
                    {
                        "type": "image_url",
                        "image_url": {"url": url}
                    }
                ]
            }
        ]
    )

    text = response.choices[0].message.content

    # GPT already sends JSON, so parse:
    try:
        data = json.loads(text)
        return data
    except:
        print("AI did not return valid JSON:")
        print(text)
        return []


all_devices = []

for rom_version, url in IMAGE_URLS.items():
    rows = extract_from_image(url)
    all_devices.extend(rows)

    # Save database
    filename = f"{rom_version}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_devices, f, indent=2, ensure_ascii=False)

    print("Done. Saved to ", filename)
