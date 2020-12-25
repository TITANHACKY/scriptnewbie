import requests
import json

class telegram_bot():
    def __init__(self):
        self.token = '1148896097:AAGupgauA433zltzx9F4E267z7BRq7MdJg4'
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    #update function to get update from the bot
    def get_updates(self, offset=None):
        url = self.base_url+"/getUpdates?timeout=100"
        if offset:
            url = url+f"&offset={offset+1}"
        r=requests.get(url)
        return json.loads(r.content)

    #send message function to send message to user
    def send_messages(self, msg, chat_id):
        url = self.base_url+f"/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown"
        requests.get(url)

    #to send photo to the user:
    def send_photo(self, photoid, chat_id):
        url =  self.base_url+f"/sendPhoto?chat_id={chat_id}&photo={photoid}"
        requests.get(url)

    def send_video(self, videoid, chat_id):
        url = self.base_url+f"/sendVideo?chat_id={chat_id}&video={videoid}"
        requests.get(url)

    def send_documents(self, documentid, chat_id):
        url = self.base_url+f"/sendDocument?chat_id={chat_id}&document={documentid}"
        requests.get(url)

    def updates(self):
        update_id = None
        while True:
            updates = telegram_bot().get_updates(offset = update_id)
            updates = updates["result"]
            if updates:
                for msgs in updates:
                    update_id = msgs["update_id"]
                    try:
                        user_id = msgs["message"]["chat"]["id"]
                        message = msgs["message"]["text"]
                        telegram_bot().send_messages(message, user_id)
                    except:
                        try:
                            photoid = msgs["message"]['phtot']['0']['file_id']
                            telegram_bot().send_photo(photoid, user_id)
                        except:
                            try:
                                videoid = msgs['message']['video']['file_id']
                                telegram_bot().send_video(videoid, user_id)
                            except:
                                try:
                                    documentid = msgs['message']['document']['file_id']
                                    telegram_bot().send_documents(documentid, user_id)
                                except:
                                    print("Error")

if __name__ == "__main__":
    telegram_bot().updates()


