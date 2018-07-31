from PIL import Image, ImageEnhance

def appendIconMark(imgIcon, imgMark, position):
    if imgIcon.mode != 'RGBA':
        imgIcon = imgIcon.convert('RGBA')

    markLayer = Image.new('RGBA', imgIcon.size, (0,0,0,0))
    markLayer.paste(imgMark, position)

    return Image.composite(markLayer, imgIcon, markLayer)

