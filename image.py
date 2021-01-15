from PIL import Image, ImageDraw, ImageFont


def create_image(width, height):
    return Image.new("RGBA", (width, height), (255, 255, 255))


def draw_point(image, x, y, color):
    ImageDraw.Draw(image).point((x, y), color)


def draw_rect(image, rect, fill=None, outline=None):
    """
    :param rect an instance of the Rectangle class
    :param fill an RGB color specified as a tuple (R,G,B) with color values in the 
                range 0-255
    :param outline color of the outline.  None means no outline.
    """
    ImageDraw.Draw(image).rectangle([rect.x1, rect.y1, rect.x2, rect.y2], fill, outline)


def save_image(image, filename):
    image.save(filename, "PNG")


def draw_text(image, text, rect):
    """
    :param rect an instance of the Rectangle class
    :param text string to render in the upper left-corner of rect in image
    """
    fontsize = 1
    font = ImageFont.truetype('Arial.ttf', fontsize)
    while font.getsize(text)[0] < (rect.x2 - rect.x1) * 0.4:
        fontsize = fontsize + 1
        font = ImageFont.truetype("Arial.ttf", fontsize)
    ImageDraw.Draw(image).text((rect.x1 + 6, rect.y1 + 5), text,
                               font=font,
                               fill=(0, 0, 0, 255))
