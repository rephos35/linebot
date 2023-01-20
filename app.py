from flask import Flask, request, abort
import json
import re
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, StickerMessage, StickerSendMessage
access_token = "5n9RrfnLskKLgSHeJkX28aZtLHbq3oJaXuujDq0AtTBlUHCNWEV0Gl42jzlMME5q8UhDBNSOHz/7Jn8ZvUNIE0FmpfJiXX7V5fi4iDHUdD7Bd6E24VhYZMSg5F3BZA0y8+z/iKbMwGFlgiNBBbACHQdB04t89/1O/w1cDnyilFU="
secret = "de6af9d6a211fccc7987c635de71f657"
ngrok_url = "https://4f54-61-231-40-109.jp.ngrok.io"
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)
app = Flask(__name__)


# verify source
@app.route("/", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body:"+ body)

    try:
        handler.handle(body, signature) # handle webhook
    except InvalidSignatureError:
        print("InvalidSignatureError. Check your channel access token/channel secret.")
        abort(400)
    return "OK"


# handle message
@handler.add(MessageEvent) # message=TextMessage
def handle_message(event):
    type = event.message.type
    if (type == "image"):
        image = line_bot_api.get_message_content(event.message.id)
        path= "./static/image/"+event.message.id+".png"
        image_url = ngrok_url+"/static/image/"+event.message.id+".png"

        with open(path, "wb") as f:
            for check in image.iter_content():
                f.write(check)
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))

    elif (type == "sticker"):
        packageId = event.message.package_id
        stickerId = event.message.sticker_id
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=packageId, sticker_id=stickerId))
    elif (type == "text"):
        message = reply_msg(event.message.text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


def reply_msg(text):
    msg_dict = {
        "Garry": "去死!",
        "IB": "<3<3<3<3<3"
    }
    local_dict = {

    }
    img_dict = {

    }
    reply_msg_content = text
    for name in msg_dict:
        if re.match(name, text):
            reply_msg_content = msg_dict[name]
    return reply_msg_content



if __name__ == "__main__":
    app.run(debug=True, port="77")