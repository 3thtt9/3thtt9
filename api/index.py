from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('wehbvXsAjKkAdS087zLKC6DnCYFIaKLKvCDDuzNU50Ys7SPGhKEiJvFynwSa7PWOwieDemi+w2huFrdPPBECaByJQo343Egu8dQesotjqOq+fdtgB2OoUS+ReAclsvmu0EG47DxPL7luCz6ZO3IOQwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9282c8e6c3c08b9ce3e8c1ea0b3e5848')

@app.route("/")
def home():
    return "LINE BOT API Server is running."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()