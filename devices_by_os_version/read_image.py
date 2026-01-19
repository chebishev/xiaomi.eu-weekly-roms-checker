import json
import openai
from dotenv import load_dotenv
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import xiaomi_eu_new_thread_checker
telegram_message = xiaomi_eu_new_thread_checker.telegram_message()

load_dotenv()
client = openai.OpenAI()

IMAGE_URLS = {
    # "MIUI 12": "https://provider.xiaomi.eu/img/devices_stable_v12_21121101.png",
    # "MIUI 13": "https://provider.xiaomi.eu/img/devices_stable_v13_23040300.png",
    # "MIUI 14": "https://provider.xiaomi.eu/img/devices_stable_v14_24011214.png",
    # "HyperOS 1.0": "https://provider.xiaomi.eu/img/devices_stable_os1_24122514.png",
    # "HyperOS 2.0": "https://provider.xiaomi.eu/img/devices_stable_os2_25070816.png",
    "HyperOS 3.0": "https://provider.xiaomi.eu/img/devices_stable_os3_26011500.png",
}


def extract_from_image(url):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},  # 🔒 THIS IS CRITICAL
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract ONLY the first 3 columns from the image.\n"
                            "Columns: codename, market_names, rom_name.\n\n"

                            "OUTPUT RULES:\n"
                            "• Output MUST be a SINGLE JSON OBJECT (dictionary)\n"
                            "• Keys = individual device names\n"
                            "• Values = {\"codename\": \"...\", \"rom_name\": \"...\"}\n\n"

                            "NORMALIZATION:\n"
                            "• If market_names contains multiple devices separated by '/' or line breaks:\n"
                            "  – SPLIT into separate keys\n"
                            "  – All share same codename and rom_name\n"
                            "• Keys MUST NOT contain '/' or new lines\n"
                            "• Trim spaces\n\n"

                            "Return ONLY valid JSON. No text."
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": url}},
                ],
            }
        ],
    )

    return json.loads(response.choices[0].message.content)


for rom_version, url in IMAGE_URLS.items():
    try:
        devices = extract_from_image(url)
    except openai.BadRequestError:
        url = telegram_message["image_url"]
        devices = extract_from_image(url)

    filename = f"{rom_version}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)

    print("Saved:", filename)