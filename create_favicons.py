# create_crown_logo.py
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 512x512 image
size = 512
img = Image.new('RGB', (size, size), '#ec4899')
draw = ImageDraw.Draw(img)

# Create gradient background
for i in range(size):
    ratio = i / size
    r = int(236 * (1 - ratio) + 139 * ratio)
    g = int(72 * (1 - ratio) + 92 * ratio)
    b = int(153 * (1 - ratio) + 246 * ratio)
    draw.rectangle([0, i, size, i+1], fill=(r, g, b))

# Draw a crown shape using polygons
# Crown base
crown_points = [
    (size//2, 80),           # top point
    (size//2 - 80, 200),     # left dip
    (size//2 - 150, 150),    # left spike
    (size//2 - 100, 280),    # left bottom
    (size//2 + 100, 280),    # right bottom
    (size//2 + 150, 150),    # right spike
    (size//2 + 80, 200),     # right dip
]
draw.polygon(crown_points, fill='white', outline='white')

# Crown base line
draw.rectangle([size//2 - 120, 280, size//2 + 120, 310], fill='white')

# Add crown details (circles on spikes)
draw.ellipse([size//2 - 170, 130, size//2 - 130, 170], fill='white')
draw.ellipse([size//2 - 30, 70, size//2 + 30, 130], fill='white')
draw.ellipse([size//2 + 130, 130, size//2 + 170, 170], fill='white')

# Add rounded corners
mask = Image.new('L', img.size, 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle((0, 0, size, size), radius=100, fill=255)
result = Image.new('RGBA', img.size)
result.paste(img, mask=mask)

# Save as PNG
result.save('zylotech-logo.png')
print("✅ Crown logo created: zylotech-logo.png")

# Create all favicon sizes
sizes = [
    (16, 'favicon-16x16.png'),
    (32, 'favicon-32x32.png'),
    (180, 'apple-touch-icon.png'),
    (192, 'android-chrome-192x192.png'),
    (512, 'android-chrome-512x512.png'),
    (150, 'mstile-150x150.png'),
]

for size_val, filename in sizes:
    resized = result.resize((size_val, size_val), Image.Resampling.LANCZOS)
    resized.save(filename)
    print(f"✅ Created: {filename}")

# Create ICO file
ico_sizes = [(16, 16), (32, 32), (48, 48)]
ico_images = [result.resize((s, s), Image.Resampling.LANCZOS) for s, _ in ico_sizes]
ico_images[0].save('favicon.ico', format='ICO', sizes=[(s, s) for s, _ in ico_sizes], append_images=ico_images[1:])
print("✅ Created: favicon.ico")

# Create manifest files
import json
manifest = {
    "name": "ZyloTech Creators Studio",
    "short_name": "ZyloTech",
    "icons": [
        {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
    ],
    "theme_color": "#0f172a",
    "background_color": "#0f172a",
    "display": "standalone",
    "start_url": "/",
    "scope": "/"
}

with open('site.webmanifest', 'w') as f:
    json.dump(manifest, f, indent=4)
print("✅ Created: site.webmanifest")

browserconfig = '''<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square150x150logo src="/mstile-150x150.png"/>
            <TileColor>#ec4899</TileColor>
        </tile>
    </msapplication>
</browserconfig>'''

with open('browserconfig.xml', 'w') as f:
    f.write(browserconfig)
print("✅ Created: browserconfig.xml")

print("\n🎉 All crown favicon files created!")