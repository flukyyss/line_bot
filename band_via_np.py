import os, time, re, urllib
from PIL import Image
import logging
import xlsxwriter


def image_similarity_bands_via_numpy(filepath1, filepath2):
    import math
    import operator
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

def get_thumbnail(image, size=(128, 128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size);  # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

workbook = xlsxwriter.Workbook('band_via_np.xlsx')
worksheet = workbook.add_worksheet()
for n in range(20):
    for r in range(30):
        test = 'test-'+str(n+1)+'.jpg'
        img = 'img-'+str(r+1)+'.jpg'
        print(n+1)
        print(r+1)
        print(image_similarity_bands_via_numpy(test,img))
        worksheet.write(0 , r+1, r+1)
        worksheet.write(n+1, 0, n+1)
        worksheet.write(n + 1, r + 1, image_similarity_bands_via_numpy(test,img))


workbook.close()
