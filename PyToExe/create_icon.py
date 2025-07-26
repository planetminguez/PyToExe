#!/usr/bin/env python3
"""
Create a red and black Python2Exe icon
"""

import os
from PIL import Image, ImageDraw, ImageFont
import subprocess

def create_icon():
    # Create a 1024x1024 image for high resolution
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    red = (220, 20, 60)  # Crimson red
    black = (20, 20, 20)  # Near black
    white = (255, 255, 255)
    
    # Create gradient background circle
    center = size // 2
    radius = size // 2 - 20
    
    # Draw outer black circle
    draw.ellipse([center - radius, center - radius, 
                  center + radius, center + radius], 
                 fill=black, outline=None)
    
    # Draw inner red circle
    inner_radius = radius - 40
    draw.ellipse([center - inner_radius, center - inner_radius,
                  center + inner_radius, center + inner_radius],
                 fill=red, outline=None)
    
    # Create Python symbol
    # Draw stylized "P" for Python
    p_width = 120
    p_height = 200
    p_x = center - 60
    p_y = center - 100
    
    # Main vertical line of P
    draw.rectangle([p_x, p_y, p_x + 40, p_y + p_height], fill=white)
    
    # Top horizontal line
    draw.rectangle([p_x, p_y, p_x + p_width, p_y + 40], fill=white)
    
    # Middle horizontal line
    draw.rectangle([p_x, p_y + 70, p_x + 80, p_y + 110], fill=white)
    
    # Right vertical line (top part)
    draw.rectangle([p_x + 80, p_y, p_x + p_width, p_y + 110], fill=white)
    
    # Add "2" symbol
    two_x = center + 20
    two_y = center - 50
    two_size = 80
    
    # Draw stylized "2"
    draw.rectangle([two_x, two_y, two_x + two_size, two_y + 25], fill=white)  # Top
    draw.rectangle([two_x + 55, two_y, two_x + two_size, two_y + 60], fill=white)  # Right top
    draw.rectangle([two_x, two_y + 35, two_x + two_size, two_y + 60], fill=white)  # Middle
    draw.rectangle([two_x, two_y + 60, two_x + 25, two_y + 100], fill=white)  # Left bottom
    draw.rectangle([two_x, two_y + 75, two_x + two_size, two_y + 100], fill=white)  # Bottom
    
    # Add "EXE" text at bottom
    try:
        # Try to use a system font
        font_size = 60
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "EXE"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center - text_width // 2
    text_y = center + 80
    
    # Draw text with black outline
    for adj_x in [-2, -1, 0, 1, 2]:
        for adj_y in [-2, -1, 0, 1, 2]:
            if adj_x != 0 or adj_y != 0:
                draw.text((text_x + adj_x, text_y + adj_y), text, font=font, fill=black)
    
    # Draw main text in white
    draw.text((text_x, text_y), text, font=font, fill=white)
    
    # Add subtle highlight
    highlight_radius = radius - 80
    draw.arc([center - highlight_radius, center - highlight_radius - 100,
              center + highlight_radius, center + highlight_radius - 100],
             -45, 45, width=8, fill=white)
    
    return img

def create_icns_file(png_path, icns_path):
    """Convert PNG to ICNS using iconutil"""
    # Create iconset directory
    iconset_dir = png_path.replace('.png', '.iconset')
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Define required sizes for iconset
    sizes = [
        (16, 'icon_16x16.png'),
        (32, 'icon_16x16@2x.png'),
        (32, 'icon_32x32.png'),
        (64, 'icon_32x32@2x.png'),
        (128, 'icon_128x128.png'),
        (256, 'icon_128x128@2x.png'),
        (256, 'icon_256x256.png'),
        (512, 'icon_256x256@2x.png'),
        (512, 'icon_512x512.png'),
        (1024, 'icon_512x512@2x.png')
    ]
    
    # Load the original image
    original = Image.open(png_path)
    
    # Create all required sizes
    for size, filename in sizes:
        resized = original.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_dir, filename))
    
    # Convert iconset to icns
    subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icns_path], check=True)
    
    # Clean up iconset directory
    subprocess.run(['rm', '-rf', iconset_dir], check=True)

def main():
    # Create the icon
    icon = create_icon()
    
    # Save as PNG first
    png_path = '/Users/minguez/Desktop/Python2Exe-DMG/Resources/Python2Exe.png'
    icon.save(png_path, 'PNG')
    print(f"Saved PNG icon: {png_path}")
    
    # Convert to ICNS
    icns_path = '/Users/minguez/Desktop/Python2Exe-DMG/Resources/Python2Exe.icns'
    create_icns_file(png_path, icns_path)
    print(f"Created ICNS icon: {icns_path}")

if __name__ == '__main__':
    main()
