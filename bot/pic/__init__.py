from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    lines = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)

    return(lines)

def render(imagePath, message) -> Image:

    # Load image
    img = Image.open(imagePath).convert("RGBA")

    # Create a scaler so that the size is about 500 x 500 pixels
    w, h = img.size
    font_size = round((w + h)/20)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', font_size)

    margin = round(w/25)
    w_limit = round(w - margin*2)

    message_wrapped = wrap_text(message, font, w_limit)

    heights = []
    for i in range(0, len(message_wrapped)):
        heights.append( font.getsize(message_wrapped[i])[1] )

    t_height = sum(heights)

    if t_height < h/2 - margin:
        offset = round(h/2) - margin
    else:
        offset = h - t_height - margin

    for line in message_wrapped:
        draw.text((margin, offset), line, font = font, stroke_width=2, stroke_fill ='black')
        offset += font.getsize(line)[1]

    # Add watermark
    wm = Image.open('./data/images/watermark transparent.png')
    a, b = wm.size

    s = w/(5*a)

    x = round(a*s)
    y = round(b*s)

    wm_resize = wm.resize((x,y))

    img.alpha_composite(wm_resize, dest = (w - x, 0))

    return(img)