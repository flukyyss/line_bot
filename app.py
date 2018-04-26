# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from flask import Flask, request, abort
import os, stat, urllib
from tempfile import NamedTemporaryFile
import json
import numpy as np
from PIL import Image
import errno
from PIL import Image

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextSendMessage, MessageEvent, ImageMessage, TextMessage, ImageSendMessage
)


LINE_API = 'https://api.line.me/v2/bot/message/reply'
handler = WebhookHandler('058e9407061ba0bf6cef25392fcd34df')
line_bot_api = LineBotApi('DXYPEtAqiUkn9e2HyPughfjyafbrCxT4nBZ52rDf1U'
                          'KDSvZcWI3G9OKgexXggWZRER9ml7RAmTUjElHzAPzBV'
                          'tVwzfXjin25UzjsJKz75TenY1BshnLWgIDbxyKZp3G1y'
                          'higMP08ihMxG6pkr6rfEQdB04t89/1O/w1cDnyilFU=')
Authorization = 'Bearer DXYPEtAqiUkn9e2HyPughfjyafbrCxT4nBZ52rDf1UKDSv' \
                'ZcWI3G9OKgexXggWZRER9ml7RAmTUjElHzAPzBVtVwzfXjin25Uzjs' \
                'JKz75TenY1BshnLWgIDbxyKZp3G1yhigMP08ihMxG6pkr6rfEQdB04' \
                't89/1O/w1cDnyilFU='
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': Authorization
  }
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
    os.chmod(static_tmp_path + '/info.txt', stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print('callback')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print('text')
    print(static_tmp_path)

    if(event.message.text == 'ขั้นตอนการลงทะเบียน'):
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(original_content_url="https://chulalongkornhospital.go.th/hr/row/row/b/images/S_5255540692607.jpg",
                                 preview_image_url="https://chulalongkornhospital.go.th/hr/row/row/b/images/S_5255540692607.jpg"),
            ]
        )
    elif(event.message.text == 'เมนู'):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ท่านสามารถเลือกเมนูจาก Bulletin ด้านล่าง'),
                TextSendMessage(text='หรือสามารถพิมพ์คำสั่งต่อไปนี้'+'\n'\
                                     ' 1.[ขั้นตอนการลงทะเบียน] เพื่อดูวิธีการลงทะเบียนออนไลน์'+'\n'\
                                     ' 2.[ติดต่อ] เพื่อดูเบอร์โทรศัพท์ของโรงพยาบาล'+'\n'\
                                     ' 3.[ลงทะเบียนผู้ป่วย] เพื่อเข้าสู่หน้าลงทะเบียนผู้ป่วยใหม่'+'\n'\
                                     ' 4.[คำถามที่พบบ่อย] เพื่อเข้าาสู่หน้า FAQ')
            ]
        )
    elif(event.message.text == 'ติดต่อ'):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='เบอร์โรงพยาบาลจุฬาลงกรณ์ : 022564000'+'\n'\
                         'เบอร์ฝ่ายมะเร็งวิทยา : 022564100')
            ]
        )
    elif(event.message.text == 'ลงทะเบียนผู้ป่วย'):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='http://chulalongkornhospital.go.th/hr/row/row/b/row3-th.php')
            ]
        )
    elif(event.message.text == 'คำถามที่พบบ่อย'):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='https://www.chulacancer.net/faq-list.php?gid=62')
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=event.message.text)
            ]
        )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):

    message_content = line_bot_api.get_message_content(event.message.id)
    with NamedTemporaryFile(dir=static_tmp_path, prefix='img-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + 'jpg'
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    im = Image.open(dist_path)
    im2 = Image.open('pat2.jpg')
    rgb_im = im.convert('RGB')
    rgb_im2 = im2.convert('RGB')
    count=0
    if(im.size[0]!=im2.size[0] & im.size[1]!=im2.size[1]):
        im.resize((im2.size[0],im2.size[1]))
        print('resize')
        print(im2.size[0])
        print(im2.size[1])
    for n in range(im2.size[0]): #
        for r in range(im2.size[1]):
            pixel1 = rgb_im.getpixel((n, r))
            pixel2 = rgb_im2.getpixel((n, r))
            color1_rgb = sRGBColor(pixel1[0],pixel1[1],pixel1[2])
            color2_rgb = sRGBColor(pixel2[0],pixel2[1],pixel2[2])
            # color1_lab = convert_color(color1_rgb, LabColor)
            # color2_lab = convert_color(color2_rgb, LabColor)
            # delta_e = delta_e_cie2000(color1_lab,color2_lab)
            # if(delta_e<15):
            #     count+=1
        if(n%10==0):
            print(n)
    print(count/(im2.size[0]*im2.size[1]))
    r, g, b = rgb_im.getpixel((1, 1))

    print(r, g, b)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'+request.host_url + os.path.join('static', 'tmp', dist_name))
            # ImageSendMessage(original_content_url="https://preview.ibb.co/fk8rE7/pat2_s.jpg",
            #                  preview_image_url="https://preview.ibb.co/fk8rE7/pat2_s.jpg"),
            # TextSendMessage(text='Breast has 620 ml with similarity 59.83 %'),
            # ImageSendMessage(original_content_url="https://preview.ibb.co/koNJu7/pat3_s.jpg",
            #                  preview_image_url="https://preview.ibb.co/koNJu7/pat3_s.jpg"),
            # TextSendMessage(text='Breast has 490 ml with similarity 68.73 %')
        ])
    '''''''''''
    line_bot_api.reply_message(
        event.reply_token, [

            ImageSendMessage(original_content_url="https://preview.ibb.co/fk8rE7/pat2_s.jpg",
                             preview_image_url="https://preview.ibb.co/fk8rE7/pat2_s.jpg"),
            TextSendMessage(text='Breast has 620 ml with similarity 59.83 %'),
            ImageSendMessage(original_content_url="https://preview.ibb.co/koNJu7/pat3_s.jpg",
                             preview_image_url="https://preview.ibb.co/koNJu7/pat3_s.jpg"),
            TextSendMessage(text='Breast has 490 ml with similarity 68.73 %')
        ]
    )
    '''''''''''

if __name__ == '__main__':
    make_static_tmp_dir()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)

