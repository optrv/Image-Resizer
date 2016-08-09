import os, configparser
from PIL import Image

conf = configparser.ConfigParser()
conf.read('image_resizer.cfg')

path_in = conf.get('OPTIONS', 'path_in') # Path of folder with input images
path_out = conf.get('OPTIONS', 'path_out') # Path of folder with output images
width = int(conf.get('OPTIONS', 'width')) # Width of image (px). NOTE: Height will be proportional to Width
folder_in = os.listdir(path_in)

# Path of watermark and position of watermark on image (optional)
path_water, pos_water = None, None

# Check if options are exist
if conf.has_option('OPTIONS', 'path_water'):
    path_water = conf.get('OPTIONS', 'path_water')
    if conf.has_option('OPTIONS', 'pos_water'):
        pos_water = conf.get('OPTIONS', 'pos_water')
    else:
        pos_water = 4 # The default value of watermark position — right below
folder_water = os.listdir(path_water)

# Watermark adding with specified (or default) value of position on image
def watermark(image_out, pos_water):
    for files in folder_water:
        if files.endswith('png') or files.endswith('jpg'):
            water = Image.open(os.path.join(path_water, files))
            if water.mode != 'RGBA':
                water = water.convert('RGBA')
            water = water.resize((image_out.size[0] // 4, \
            int((image_out.size[0] // 4 * water.size[1]) // water.size[0])), Image.BILINEAR)
            layer = Image.new('RGBA', image_out.size, (0, 0, 0, 0))
            place = {1: (10, 10), 2: (image_out.size[0] - 10 - water.size[0], 10), 3: (10, \
                    image_out.size[1] - 10 - water.size[1]), 4: (image_out.size[0] - 10 - \
                    water.size[0], image_out.size[1] - 10 - water.size[1])}
            pos_water = (place[int(pos_water)])
            layer.paste(water,(pos_water))
            image_out = Image.composite(layer, image_out, layer)
            break # Just first one watermark image in the specified folder
    return image_out

print()
for image_in in folder_in:
    if not image_in.startswith('.') and image_in != 'Thumbs.db':
        print('Resizing image' + ' ' + image_in)
        image_out = Image.open(os.path.join(path_in, image_in))
        if image_out.mode != 'RGBA':
            image_out = image_out.convert('RGBA')

        # Resize image proportional to specified width
        image_out = image_out.resize((width, int((width * image_out.size[1]) / \
                    image_out.size[0])), Image.BILINEAR)

        # Save image. Make output-folder if it's not exists
        if not os.path.exists(path_out):
            os.makedirs(path_out)
            if path_water != None and pos_water != None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out, 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out, 'resized-' + image_in))
        # Just save image
        else:
            if path_water != None and pos_water != None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out, 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out, 'resized-' + image_in))
print()
print('Batch resizing (& watermarking) processing complete.')