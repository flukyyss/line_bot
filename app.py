from __future__ import unicode_literals
from flask import Flask, request, abort
import os
import sys
import errno
import tempfile
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, MessageEvent, ImageMessage, TextMessage
)

import json
import requests
LINE_API = 'https://api.line.me/v2/bot/message/reply'
handler = WebhookHandler('058e9407061ba0bf6cef25392fcd34df')
line_bot_api = LineBotApi('DXYPEtAqiUkn9e2HyPughfjyafbrCxT4nBZ52rDf1UKDSvZcWI3G9OKgexXggWZRER9ml7RAmTUjElHzAPzBVtVwzfXjin25UzjsJKz75TenY1BshnLWgIDbxyKZp3G1yhigMP08ihMxG6pkr6rfEQdB04t89/1O/w1cDnyilFU=')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


app = Flask(__name__)
@app.route('/')
def index():
  return "Hello World!"


@app.route('/callback', methods=['POST'])
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

@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Test.')
        ]
    )


@handler.add(MessageEvent, message = ImageMessage)
def handle_image_message(event):

    message_content = line_bot_api.get_message_content(event.message.id)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='image!')
        ])
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='File found')])
    try:
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, delete=False) as f:
            f.write(b'hello')
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='File found')])
    except:
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='ERROR')])


    tempfile_path = f.name
    #os.rename(tempfile_path,dist_path)



    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='hello2'),
            TextSendMessage(text=tempfile_path)
        ])


if __name__ == '__main__':
    make_static_tmp_dir()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
