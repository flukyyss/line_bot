import os, time, re, urllib
from PIL import Image
import logging
import xlsxwriter

def image_similarity_vectors_via_numpy(filepath1, filepath2):
    # source: http://www.syntacticbayleaves.com/2008/12/03/determining-image-similarity/
    # may throw: Value Error: matrices are not aligned .
    from numpy import average, linalg, dot
    import sys

    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    image1 = get_thumbnail(image1, stretch_to_fit=True)
    image2 = get_thumbnail(image2, stretch_to_fit=True)

    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # ValueError: matrices are not aligned !
    res = dot(a / a_norm, b / b_norm)
    return res

def get_thumbnail(image, size=(128, 128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size);  # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

workbook = xlsxwriter.Workbook('vector_via_numpy.xlsx')
worksheet = workbook.add_worksheet()
for n in range(40):
    for r in range(30):
        test = 'test-'+str(n+1)+'.jpg'
        img = 'img-'+str(r+1)+'.jpg'
        worksheet.write(0, r + 1, r + 1)
        worksheet.write(n + 1, 0, n + 1)
        worksheet.write(n + 1, r + 1, image_similarity_vectors_via_numpy(test, img))
    print(n)

workbook.close()