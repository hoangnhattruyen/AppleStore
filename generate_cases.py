import os
from PIL import Image, ImageDraw, ImageFilter

CASES_DIR = os.path.join(os.path.dirname(__file__), "shop", "static", "images", "cases")
os.makedirs(CASES_DIR, exist_ok=True)

COLORS = [
    {"slug": "lake-green", "name": "Lake Green", "base": "#2e5b56", "bump": "#3d736c", "dark": "#1d3d39", "light": "#46857e"},
    {"slug": "denim", "name": "Denim", "base": "#394d68", "bump": "#4c668a", "dark": "#27364b", "light": "#54739c"},
    {"slug": "light-pink", "name": "Light Pink", "base": "#f1c3cb", "bump": "#dfa5b0", "dark": "#ce8f9b", "light": "#fae3e7"},
    {"slug": "plum", "name": "Plum", "base": "#4a293a", "bump": "#65374f", "dark": "#311825", "light": "#76435e"},
    {"slug": "starfruit", "name": "Starfruit", "base": "#e7e279", "bump": "#cac458", "dark": "#adab3c", "light": "#f3f0a4"},
    {"slug": "stone-gray", "name": "Stone Gray", "base": "#76797d", "bump": "#8f9397", "dark": "#55585b", "light": "#9fa3a7"},
    {"slug": "black", "name": "Black", "base": "#1e1e1e", "bump": "#333333", "dark": "#121212", "light": "#444444"},
    {"slug": "product-red", "name": "PRODUCT(RED)", "base": "#c81e26", "bump": "#e6353e", "dark": "#9b131a", "light": "#e8474e"},
    {"slug": "ultramarine", "name": "Ultramarine", "base": "#264875", "bump": "#355e96", "dark": "#1a3253", "light": "#416ea8"},
    {"slug": "white", "name": "White", "base": "#f4f4f6", "bump": "#e2e2e6", "dark": "#d0d0d5", "light": "#ffffff"},
]


def hex_to_rgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def make_case_image(color, variant):
    img = Image.new("RGBA", (420, 680), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    base = hex_to_rgb(color["base"])
    bump = hex_to_rgb(color["bump"])
    dark = hex_to_rgb(color["dark"])
    light = hex_to_rgb(color["light"])

    body = (45, 30, 375, 650)
    draw.rounded_rectangle(body, radius=62, fill=base)
    draw.rounded_rectangle((54, 40, 366, 640), radius=54, outline=(255, 255, 255, 60), width=3)

    if variant == "back":
        camera_bump = (72, 54, 192, 190)
        draw.rounded_rectangle(camera_bump, radius=34, fill=bump)
        draw.rounded_rectangle((78, 60, 186, 184), radius=28, outline=(255, 255, 255, 60), width=2)

        lens_positions = [(96, 84), (96, 150), (156, 117)]
        for x, y in lens_positions:
            draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(20, 20, 22, 255), outline=dark, width=4)
            draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(10, 10, 12, 255), outline=(80, 80, 90, 255), width=2)
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 255, 255, 120))

        draw.ellipse((153, 58, 171, 76), fill=(245, 245, 220, 255), outline=(200, 200, 200, 200), width=2)
        draw.ellipse((152, 148, 166, 162), fill=(24, 24, 24, 255), outline=(90, 90, 90, 200), width=2)
        draw.rounded_rectangle((328, 215, 338, 256), radius=5, fill=(255, 255, 255, 200))

        draw.text((210, 320), "", fill=(dark[0], dark[1], dark[2], 180), anchor="mm", font=None)
    else:
        draw.rounded_rectangle((58, 42, 362, 638), radius=52, outline=(255, 255, 255, 70), width=2)
        ring_color = (255, 255, 255, 115)
        draw.ellipse((142, 252, 278, 388), outline=ring_color, width=6)
        draw.ellipse((156, 266, 264, 374), outline=(255, 255, 255, 80), width=2)
        draw.rounded_rectangle((182, 392, 238, 424), radius=6, fill=(255, 255, 255, 95))
        draw.text((210, 305), "MagSafe", fill=(255, 255, 255, 120), anchor="mm")
        draw.text((210, 510), "Designed by Apple", fill=(255, 255, 255, 90), anchor="mm")

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((55, 40, 365, 645), radius=62, fill=(0, 0, 0, 55))
    img = Image.alpha_composite(img, shadow)
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    return img


for c in COLORS:
    back = make_case_image(c, "back")
    inside = make_case_image(c, "inside")
    back.save(os.path.join(CASES_DIR, f"case-{c['slug']}-back.png"), format="PNG")
    inside.save(os.path.join(CASES_DIR, f"case-{c['slug']}-inside.png"), format="PNG")

print(f"Generated {len(COLORS)} PNG case images in {CASES_DIR} successfully!")
