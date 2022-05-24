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

line_bot_api = LineBotApi('epyIeACG8dIWFZruh4AK7Xg4mjDQe3q/XEkPyPeYbQeiWQQYbZoi82FNoYOqy8RHRHc+ZKQmMJKlDgWMSwItoJXJ1UEkqo91UpF+kuClntMLhSXclaIiKcM2oJk/WyE4/K4v9oOLSyolVk3Pq0/IIQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ac774d17ba0db99b6911a163c8b5c892')


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