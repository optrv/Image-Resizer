import os, argparse
from PIL import Image

pars = argparse.ArgumentParser(description='Image Resizer parameters.')
# Arguments definition

pars.add_argument('path_in', metavar='PATH_IN', type = str, nargs = 1,
                  help='Path of folder with input images.')
pars.add_argument('path_out', metavar='PATH_OUT', type=str, nargs = 1,
                  help='Path of folder with output images.')
pars.add_argument('width', metavar='WIDTH', type=int, nargs=1,
                  help='Width of image (px). NOTE: Height will be \
                  proportional to Width.')
pars.add_argument('-wat', metavar=('WATERMARK_PATH'), type=str, nargs= 1,
                  help='Path of folder with watermark')
pars.add_argument('--pos', metavar=('WATERMARK_POSITION.'), type=str, nargs=1,
                  help='Position of Watermark on image: 1: left above. \
                  2: right above. 3: left below. 4: right below. DEFAULT: 4: right below.')
args = pars.parse_args()

path_in = args.path_in # Path of folder with input images
path_out = args.path_out # Path of folder with output images
width = args.width[0] # Width of image (px). NOTE: Height will be proportional to Width
folder_in = os.listdir(path_in[0])

# Path of watermark and position of watermark on image
path_water, pos_water = None, None

# Check if optional arguments are exist
if args.wat != None:
    path_water = args.wat
    if args.pos != None:
        pos_water = args.pos[0]
    else:
        pos_water = 4 # The default value of watermark position — right below
    folder_water = os.listdir(path_water[0])

# Watermark adding with specified (or default) value of position on image
def watermark(image_out, pos_water):
    for files in folder_water:
        if files.endswith('png') or files.endswith('jpg'):
            water = Image.open(os.path.join(path_water[0], files))
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
        image_out = Image.open(os.path.join(path_in[0], image_in))
        if image_out.mode != 'RGBA':
            image_out = image_out.convert('RGBA')

        # Resize image proportional to specified width
        image_out = image_out.resize((width, int((width * image_out.size[1]) / \
                    image_out.size[0])), Image.BILINEAR)

        # Save image. Make output-folder if it's not exists
        if not os.path.exists(path_out[0]):
            os.makedirs(path_out[0])
            if path_water != None and pos_water != None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out[0], 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out[0], 'resized-' + image_in))
        # Just save image
        else:
            if path_water != None and pos_water != None:
                image_out = watermark(image_out, pos_water)
                image_out.save(os.path.join(path_out[0], 'resized+watermark-' + image_in))
            else:
                image_out.save(os.path.join(path_out[0], 'resized-' + image_in))
print()
print('Batch resizing (& watermarking) processing complete.')