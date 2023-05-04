import openai
import os

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
webhook_handler = WebhookHandler('9282c8e6c3c08b9ce3e8c1ea0b3e5848')

# 設定 OpenAI API 密鑰
openai.api_key = "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"
# openai.api_key = "OPENAI_API_KEY"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300

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
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )

    # 取得生成的文本
    output_text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))


if __name__ == "__main__":
    app.run()