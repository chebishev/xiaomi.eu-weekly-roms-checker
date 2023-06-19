import sourceforge_new_folder_checker
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

# get your api_id, api_hash, token from telegram
api_id = int(input("Enter your api_id: "))
api_hash = input("Enter your api_hash: ")
token = input("Enter your token: ")
message = sourceforge_new_folder_checker.telegram_message()

# your phone number
phone = input("Enter your phone number: ")

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
    client.send_code_request(phone)

    # signing in the client
    client.sign_in(phone, input('Enter the code: '))

try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    receiver = InputPeerUser(int(input("Enter your user_id: ")), int(input("Enter your access_hash or just 0: ")))

    # sending message using telegram client
    client.send_message(receiver, message, parse_mode='html')
except Exception as e:

    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e)

# disconnecting the telegram session
client.disconnect()