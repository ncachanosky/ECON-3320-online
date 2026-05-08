"""
favicon_generator.py
Generates favicon.ico for Money, Institutions, and Markets

Design: copper "M" monogram on charcoal background — EO palette
Output: favicon.ico (16x16, 32x32, 48x48) + favicon.png (32x32)

Requirements: pip install Pillow

Run from project root:
    python favicon_generator.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

# EO palette
CHARCOAL = (54, 69, 79)     # #36454F — background
COPPER   = (184, 115, 51)   # #B87333 — monogram and border


def make_favicon_image(size):
    img = Image.new("RGBA", (size, size), CHARCOAL)
    draw = ImageDraw.Draw(img)

    # Subtle copper border
    b = max(1, size // 16)
    draw.rectangle([b, b, size - b - 1, size - b - 1], outline=COPPER, width=b)

    # "M" monogram
    font_size = int(size * 0.60)
    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
    ]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, font_size)
                break
            except Exception:
                continue

    if font is None:
        font = ImageFont.load_default()

    letter = "M"
    bbox = draw.textbbox((0, 0), letter, font=font)
    x = (size - (bbox[2] - bbox[0])) // 2 - bbox[0]
    y = (size - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((x, y), letter, fill=COPPER, font=font)

    return img


def generate_favicon(output_path="favicon.ico"):
    sizes = [16, 32, 48]
    images = [make_favicon_image(s) for s in sizes]

    images[0].save(
        output_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print(f"Saved: {output_path}  ({sizes}px)")

    png_path = output_path.replace(".ico", ".png")
    images[1].save(png_path, format="PNG")
    print(f"Saved: {png_path}  (32x32 PNG)")


if __name__ == "__main__":
    generate_favicon("favicon.ico")