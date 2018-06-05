import os, time, re, urllib
from PIL import Image
import logging
from functools import reduce
import xlsxwriter

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

def get_thumbnail(image, size=(128, 128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size);  # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

workbook = xlsxwriter.Workbook('histogram_via_pil.xlsx')
worksheet = workbook.add_worksheet()
for n in range(20):
    for r in range(30):
        test = 'test-'+str(n+1)+'.jpg'
        img = 'img-'+str(r+1)+'.jpg'
        print(n+1)
        print(r+1)
        print(image_similarity_histogram_via_pil(test,img))
        worksheet.write(0, r + 1, r + 1)
        worksheet.write(n + 1, 0, n + 1)
        worksheet.write(n + 1, r + 1, image_similarity_histogram_via_pil(test, img))

workbook.close()