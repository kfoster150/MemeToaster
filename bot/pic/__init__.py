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

def render(imageBinary, caption) -> Image:

    # Load image
    img = Image.open(imageBinary).convert("RGBA")

    # Text scaling:
    # Font size ~= (image width + image height)/20
    # Font line width ~= (font size)/25
    w, h = img.size
    font_size = round((w + h)/20)

    stroke_width = round(font_size/25)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('./data/fonts/arial.ttf', font_size)

    margin = round(w/25)
    w_limit = round(w - margin*2)

    caption_wrapped = wrap_text(caption, font, w_limit)

    heights = []
    for i in range(0, len(caption_wrapped)):
        heights.append( font.getsize(caption_wrapped[i])[1] )

    t_height = sum(heights)

    if t_height < h/2 - margin:
        offset = round(h/2) - margin
    else:
        offset = h - t_height - margin

    for line in caption_wrapped:
        draw.text((margin, offset), line, font = font, stroke_width=stroke_width, stroke_fill ='black')
        offset += font.getsize(line)[1]

    # Add watermark
    wm = Image.open('./data/images/watermark transparent.png')
    a, b = wm.size

    s = w/(5*a)

    x = round(a*s)
    y = round(b*s)

    wm_resize = wm.resize((x,y))

    img.alpha_composite(wm_resize, dest = (w - x, 0))
    img = img.convert("RGB")

    return(img)
