import os, time, re, urllib
from PIL import Image
import logging
import xlsxwriter


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

workbook = xlsxwriter.Workbook('greyscale_hash_code.xlsx')
worksheet = workbook.add_worksheet()
for n in range(20):
    for r in range(30):
        test = 'test-'+str(n+1)+'.jpg'
        img = 'img-'+str(r+1)+'.jpg'
        print(n+1)
        print(r+1)
        print(image_similarity_greyscale_hash_code(test,img))
        worksheet.write(0, r + 1, r + 1)
        worksheet.write(n + 1, 0, n + 1)
        worksheet.write(n + 1, r + 1, image_similarity_greyscale_hash_code(test, img))
    print(n)

workbook.close()