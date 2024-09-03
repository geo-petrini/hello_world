from flask import Blueprint
from flask import jsonify
from flask import request
from flask import send_file
from colorhash import ColorHash
from PIL import Image
import io

api = Blueprint('api', __name__)

@api.route('/dashboard')
def dashboard():
    return "API Dashboard"

@api.route('/<input>')
def generate(input):
    out = {}
    colors = []
    for char in input:
        c = ColorHash(char)
        colors.append(c.hex)
    out['colors'] = colors
    out['input'] = input
    output = request.args['output'] if 'output' in request.args else None
    block_size = int(request.args['block_size']) if 'block_size' in request.args else None
    if output and output.lower() == 'image':
        if block_size:
            image = generate_image(colors, block_size)
        else:
            image = generate_image(colors)
        
        return send_file(image, mimetype='image/png')

    return jsonify(out)


def generate_image(colors: list, block_size:int=20):
    # Define image dimensions
    block_width = block_size
    block_height = block_width
    image_width = block_width * len(colors)
    image_height = block_height

    # Create a new image
    image = Image.new("RGB", (image_width, image_height))

    # Draw the colors as blocks
    for i, color in enumerate(colors):
        for x in range(i * block_width, (i + 1) * block_width):
            for y in range(image_height):
                image.putpixel((x, y), Image.new("RGB", (1, 1), color).getpixel((0, 0)))

    # Save or display the image
    #image.show()  # To display the image
    #image.save("colors.png")  # To save the image
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)  # Seek to the start of the stream
    return img_io
