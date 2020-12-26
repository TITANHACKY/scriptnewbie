import requests
import json

class telegram_bot():
    def __init__(self):
        self.token = '1148896097:AAGupgauA433zltzx9F4E267z7BRq7MdJg4'
        self.chat_id = 1037166796
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    #getting updates
    def get_updates(self, offset=None):
        url = self.base_url+"/getUpdates?timeout=100"
        if offset:
            url = url+f"&offset={offset+1}"
        r=requests.get(url)
        return json.loads(r.content)

    #forwarding the message
    def forward_message(self, from_chat_id, msgid):
        url = self.base_url+f"/forwardMessage?chat_id={self.chat_id}&from_chat_id={from_chat_id}&message_id={msgid}"
        requests.get(url)

    def send_messages(self, msg, chat_id):
        url = self.base_url+f"/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown"
        print(url)
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
                        from_chat_id = msgs["message"]["chat"]["id"]
                        msgid = msgs["message"]["message_id"]
                        chat_id = self.chat_id
                        if(from_chat_id==chat_id):
                            try:
                                message = msgs["message"]["text"]
                                reply_to_chatid = msgs["message"]["reply_to_message"]["forward_from"]["id"]
                                telegram_bot().send_messages(message, reply_to_chatid)
                            except:
                                try:
                                    reply_to_chatid = msgs["message"]["reply_to_message"]["forward_from"]["id"]
                                    photoid = msgs["message"]['photo']['0']['file_id']
                                    telegram_bot().send_photo(photoid, reply_to_chatid)
                                except:
                                    try:
                                        reply_to_chatid = msgs["message"]["reply_to_message"]["forward_from"]["id"]
                                        videoid = msgs['message']['video']['file_id']
                                        telegram_bot().send_video(videoid, reply_to_chatid)
                                    except:
                                        try:
                                            reply_to_chatid = msgs["message"]["reply_to_message"]["forward_from"]["id"]
                                            documentid = msgs['message']['document']['file_id']
                                            telegram_bot().send_documents(documentid, reply_to_chatid)
                                        except:
                                            message=''
                        else:
                            telegram_bot().forward_message(from_chat_id,msgid)
                    except:
                        print('error')

if __name__ == "__main__":
    telegram_bot().updates()