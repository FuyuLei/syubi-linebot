import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage,
    ImageSendMessage)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/version')
def version():
    return '1.0'


@app.route('/<user>')
def hello_user(user):
    return 'Hello {}, nice to meet you'.format(user)


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
        abort(400)

    return 'OK'


def push_message(event):
    userId = line_bot_api.get_profile(user_id)
    groupId = line_bot_api.get_profile(group_id)

    if event.source.type == 'group':
        line_bot_api.push_message(groupId, TextSendMessage(text='安安'))
    return

    line_bot_api.push_message(userId, TextSendMessage(text='安安'))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg == '企鵝掰掰' and event.source.type == 'group':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='大家掰掰OUO/'))
        line_bot_api.leave_group(event.source.group_id)
    return

    if msg == '企鵝':
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://i.imgur.com/pe3lDkS.jpg',
                             preview_image_url='https://i.imgur.com/pe3lDkS.jpg'))
    return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Sticker'))


if __name__ == '__main__':
    app.run()
