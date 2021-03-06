# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from flask import Flask, request, abort
import os, stat, urllib
from tempfile import NamedTemporaryFile
import json
import numpy as np
import math
from skimage import io, color
import errno
from PIL import Image
from functools import reduce


from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff_matrix import delta_e_cie2000
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
                TextSendMessage(text='ไม่รู้จักคำว่า ' + event.message.text),
                TextSendMessage(text='ลองพิมพ์ [เมนู] ดูนะครับ')
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

    print('1')

    imgurl = ["https://image.ibb.co/niNnOT/img_1.jpg","https://image.ibb.co/d0Du3T/img_2.jpg","https://image.ibb.co/fbyGHo/img_3.jpg","https://image.ibb.co/fcjZ3T/img_4.jpg","https://image.ibb.co/fvGgiT/img_5.jpg",
              "https://image.ibb.co/f4kwHo/img_6.jpg","https://image.ibb.co/kNe1iT/img_7.jpg","https://image.ibb.co/kq1sq8/img_8.jpg","https://preview.ibb.co/fvLJV8/img_9.jpg","https://preview.ibb.co/cP6E3T/img_10.jpg",
              "https://preview.ibb.co/hfawHo/img_11.jpg","https://image.ibb.co/gZBsq8/img_12.jpg","https://image.ibb.co/feDixo/img_13.jpg","https://preview.ibb.co/fBrsq8/img_14.jpg","https://preview.ibb.co/c7CMiT/img_15.jpg",
              "https://preview.ibb.co/iJMsq8/img_16.jpg","https://preview.ibb.co/f3CXq8/img_17.jpg","https://preview.ibb.co/e2F7OT/img_18.jpg","https://preview.ibb.co/mcKqco/img_19.jpg","https://preview.ibb.co/gksXq8/img_20.jpg",
              "https://preview.ibb.co/fsiBiT/img_21.jpg","https://preview.ibb.co/dLuvA8/img_22.jpg","https://preview.ibb.co/cBDYxo/img_23.jpg","https://preview.ibb.co/f2k2q8/img_24.jpg","https://preview.ibb.co/eS2hq8/img_25.jpg",
              "https://preview.ibb.co/ctYNq8/img_26.jpg","https://preview.ibb.co/jVMmHo/img_27.jpg","https://preview.ibb.co/cWbaA8/img_28.jpg","https://preview.ibb.co/c27FA8/img_29.jpg","https://preview.ibb.co/kPR8V8/img_30.jpg"]

    breast_vol = [360,370,310,600,450,470,470,580,630,530,550,500,480,540,540,410,550,420,420,570,500,510,520,500,460,440,360,430,420,490]

    def image_similarity_bands_via_numpy(filepath1, filepath2):
        import numpy
        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

        # create thumbnails - resize em
        image1 = get_thumbnail(image1)
        image2 = get_thumbnail(image2)

        # this eliminated unqual images - though not so smarts....
        if image1.size != image2.size or image1.getbands() != image2.getbands():
            return -1
        s = 0
        for band_index, band in enumerate(image1.getbands()):
            m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
            m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
            s += numpy.sum(numpy.abs(m1 - m2))
        return s

    def image_similarity_histogram_via_pil(filepath1, filepath2):
        from PIL import Image
        import math
        import operator

        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

        image1 = get_thumbnail(image1)
        image2 = get_thumbnail(image2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        rms = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return rms




    def image_similarity_greyscale_hash_code(filepath1, filepath2):
        # source: http://blog.safariflow.com/2013/11/26/image-hashing-with-python/

        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

        image1 = get_thumbnail(image1, greyscale=True)
        image2 = get_thumbnail(image2, greyscale=True)

        code1 = image_pixel_hash_code(image1)
        code2 = image_pixel_hash_code(image2)
        # use hamming distance to compare hashes
        res = hamming_distance(code1, code2)
        return res

    def image_pixel_hash_code(image):
        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))  # '00010100...'
        hexadecimal = int(bits, 2).__format__('016x').upper()
        return hexadecimal


    def hamming_distance(s1, s2):
        len1, len2 = len(s1), len(s2)
        if len1 != len2:
            "hamming distance works only for string of the same length, so i'll chop the longest sequence"
            if len1 > len2:
                s1 = s1[:-(len1 - len2)]
            else:
                s2 = s2[:-(len2 - len1)]
        assert len(s1) == len(s2)
        return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])

    def get_thumbnail(image, size=(128, 128), stretch_to_fit=False, greyscale=False):
        " get a smaller version of the image - makes comparison much faster/easier"
        if not stretch_to_fit:
            image.thumbnail(size, Image.ANTIALIAS)
        else:
            image = image.resize(size);  # for faster computation
        if greyscale:
            image = image.convert("L")  # Convert it to grayscale.
        return image

    def flat(*nums):
        'Build a tuple of ints from float or integer arguments. Useful because PIL crop and resize require integer points.'

        return tuple(int(round(n)) for n in nums)

    class Size(object):
        def __init__(self, pair):
            self.width = float(pair[0])
            self.height = float(pair[1])

        @property
        def aspect_ratio(self):
            return self.width / self.height

        @property
        def size(self):
            return flat(self.width, self.height)

    def cropped_thumbnail(img, size=(128,128)):
        '''
        Builds a thumbnail by cropping out a maximal region from the center of the original with
        the same aspect ratio as the target size, and then resizing. The result is a thumbnail which is
        always EXACTLY the requested size and with no aspect ratio distortion (although two edges, either
        top/bottom or left/right depending whether the image is too tall or too wide, may be trimmed off.)
        '''

        original = Size(img.size)
        target = Size(size)

        if target.aspect_ratio > original.aspect_ratio:
            # image is too tall: take some off the top and bottom
            scale_factor = target.width / original.width
            crop_size = Size((original.width, target.height / scale_factor))
            top_cut_line = (original.height - crop_size.height) / 2
            img = img.crop(flat(0, top_cut_line, crop_size.width, top_cut_line + crop_size.height))
        elif target.aspect_ratio < original.aspect_ratio:
            # image is too wide: take some off the sides
            scale_factor = target.height / original.height
            crop_size = Size((target.width / scale_factor, original.height))
            side_cut_line = (original.width - crop_size.width) / 2
            img = img.crop(flat(side_cut_line, 0, side_cut_line + crop_size.width, crop_size.height))

        return img.resize(target.size, Image.ANTIALIAS)


    print('2')
    similarity0 = []
    similarity = []
    similarity2 = []
    for r in range(30):
        base_img = 'img-' + str(r + 1) + '.jpg'
        similarity0.append((image_similarity_bands_via_numpy(dist_path,base_img)))
        similarity.append((image_similarity_greyscale_hash_code(dist_path,base_img)))
        similarity2.append((image_similarity_histogram_via_pil(dist_path,base_img)))

    minsim0 = min(similarity0)
    indexmin0 = similarity0.index(minsim0)
    minsim = min(similarity)
    indexmin = similarity.index(minsim)
    print('3')
    secondsim = min(similarity2)
    indexsecond = similarity2.index(secondsim)
    # secondsim = min(n for n in similarity if n != minsim)
    # indexsecond = similarity.index(secondsim)




    line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='Using 1)Bands via Numpy'+'\n'+'2)Greyscale Hash Code'+'\n'+'3)RGB Histogram'),
                ImageSendMessage(original_content_url=imgurl[indexmin0],
                                 preview_image_url=imgurl[indexmin0]),
                ImageSendMessage(original_content_url=imgurl[indexmin],
                                preview_image_url=imgurl[indexmin]),
            ImageSendMessage(original_content_url=imgurl[indexsecond],
                             preview_image_url=imgurl[indexsecond]),
            TextSendMessage(text='Respectively, Breast Volumes are %d , %d , %d'%(breast_vol[indexmin0],breast_vol[indexmin],breast_vol[indexsecond]))
        ])
    print(similarity)
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
def euclid_dist(r1,g1,b1,r2,g2,b2):
    res = math.sqrt((2*(r2-r1)*(r2-r1)+4*(g2-g1)*(g2-g1)+3*(b2-b1)*(b2-b1))+((r2+r1)/2)*((r2-r1)*(r2-r1)-(b2-b1)*(b2-b1))/256)
    return res

if __name__ == '__main__':
    make_static_tmp_dir()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)

