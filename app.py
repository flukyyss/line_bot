from __future__ import unicode_literals, print_function
from flask import Flask, request, abort
import os
import sys
from tempfile import mktemp

import errno
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


LINE_API = 'https://api.line.me/v2/bot/message/reply'
handler = WebhookHandler('058e9407061ba0bf6cef25392fcd34df')
line_bot_api = LineBotApi('DXYPEtAqiUkn9e2HyPughfjyafbrCxT4nBZ52rDf1U'
                          'KDSvZcWI3G9OKgexXggWZRER9ml7RAmTUjElHzAPzBV'
                          'tVwzfXjin25UzjsJKz75TenY1BshnLWgIDbxyKZp3G1y'
                          'higMP08ihMxG6pkr6rfEQdB04t89/1O/w1cDnyilFU=')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

def create_file():
    img_tmp = mktemp(dir=r'C:\Users\fluky\Desktop', prefix='img-', suffix='.jpg')
    f = open(img_tmp, 'w')
    f.write('hello')
    f.close()

def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

app = Flask(__name__)
@app.route ('/')
def index():
    return "Hello World!"


@app.route('/callback', methods=['POST'])
def callback():
    print('callback')
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
    print('text')
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text=event.message.text)
        ]
    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print('image')
    count = 0
    message_content = line_bot_api.get_message_content(event.message.id)


if __name__ == '__main__':
    create_file()
    make_static_tmp_dir()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
