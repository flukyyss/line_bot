from PIL import Image

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
img = Image.new( 'RGB', (250,250), "black") # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every col:
    for j in range(img.size[1]):    # For every row
        pixels[i,j] = (i, j, 100) # set the colour accordingly

# Red Color
color1_rgb = sRGBColor(pixels[0,0][0],pixels[0,0][1],pixels[0,0][2],is_upscaled=True)

# Blue Color
color2_rgb = sRGBColor(pixels[50,50][0],pixels[50,50][1],pixels[50,50][2],is_upscaled=True)

# Convert from RGB to Lab Color Space
color1_lab = convert_color(color1_rgb, LabColor);

# Convert from RGB to Lab Color Space
color2_lab = convert_color(color2_rgb, LabColor);

# Find the color difference
delta_e = delta_e_cie2000(color1_lab, color2_lab);

print ("The difference between the 2 color = ", delta_e)

img.show()