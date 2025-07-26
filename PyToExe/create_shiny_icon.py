#!/usr/bin/env python3
"""
Create a shiny red and black metallic ICNS icon with premium effects
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import math

def create_gradient(width, height, color1, color2, direction='vertical'):
    """Create a gradient between two colors"""
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    
    return gradient

def create_radial_gradient(size, center, inner_color, outer_color, radius):
    """Create a radial gradient"""
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    
    for y in range(size):
        for x in range(size):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            if distance <= radius:
                ratio = distance / radius
                r = int(inner_color[0] * (1 - ratio) + outer_color[0] * ratio)
                g = int(inner_color[1] * (1 - ratio) + outer_color[1] * ratio)
                b = int(inner_color[2] * (1 - ratio) + outer_color[2] * ratio)
                draw.point((x, y), (r, g, b))
            else:
                draw.point((x, y), outer_color)
    
    return img

def create_shiny_icon():
    """Create a shiny red and black metallic icon"""
    print("🌟 Creating shiny red and black metallic icon...")
    
    size = 1024
    center = size // 2
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Define premium colors
    deep_black = (15, 15, 15)
    metallic_black = (40, 40, 40)
    dark_red = (120, 20, 20)
    metallic_red = (200, 30, 30)
    bright_red = (255, 60, 60)
    shine_red = (255, 120, 120)
    highlight_white = (255, 255, 255)
    
    # Create base circular background with metallic gradient
    base_radius = size // 2 - 20
    base_gradient = create_radial_gradient(size, (center, center), metallic_black, deep_black, base_radius)
    
    # Create circular mask for base
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([center - base_radius, center - base_radius,
                       center + base_radius, center + base_radius], fill=255)
    
    # Apply base gradient with mask
    img.paste(base_gradient, (0, 0))
    img.putalpha(mask)
    
    # Create inner red metallic circle
    inner_radius = base_radius - 60
    red_gradient = create_radial_gradient(size, (center, center), bright_red, dark_red, inner_radius)
    
    # Create mask for inner circle
    inner_mask = Image.new('L', (size, size), 0)
    inner_mask_draw = ImageDraw.Draw(inner_mask)
    inner_mask_draw.ellipse([center - inner_radius, center - inner_radius,
                            center + inner_radius, center + inner_radius], fill=255)
    
    # Create red metallic layer
    red_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    red_layer.paste(red_gradient, (0, 0))
    red_layer.putalpha(inner_mask)
    
    # Blend red layer with base
    img = Image.alpha_composite(img, red_layer)
    
    # Add Python "P" symbol with metallic effect
    p_width = 180
    p_height = 300
    p_x = center - 90
    p_y = center - 150
    
    # Create P shape with gradient
    p_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(p_layer)
    
    # Main vertical bar of P
    p_draw.rectangle([p_x, p_y, p_x + 60, p_y + p_height], fill=highlight_white)
    
    # Top horizontal bar
    p_draw.rectangle([p_x, p_y, p_x + p_width, p_y + 60], fill=highlight_white)
    
    # Middle horizontal bar
    p_draw.rectangle([p_x, p_y + 100, p_x + 140, p_y + 160], fill=highlight_white)
    
    # Right vertical bar (top part only)
    p_draw.rectangle([p_x + 120, p_y, p_x + p_width, p_y + 160], fill=highlight_white)
    
    # Add "2" with metallic effect
    two_x = center + 40
    two_y = center - 80
    two_size = 120
    
    # Draw stylized "2"
    p_draw.rectangle([two_x, two_y, two_x + two_size, two_y + 35], fill=highlight_white)  # Top
    p_draw.rectangle([two_x + 85, two_y, two_x + two_size, two_y + 80], fill=highlight_white)  # Right top
    p_draw.rectangle([two_x, two_y + 45, two_x + two_size, two_y + 80], fill=highlight_white)  # Middle
    p_draw.rectangle([two_x, two_y + 80, two_x + 35, two_y + 120], fill=highlight_white)  # Left bottom
    p_draw.rectangle([two_x, two_y + 85, two_x + two_size, two_y + 120], fill=highlight_white)  # Bottom
    
    # Apply metallic gradient to P and 2
    p_gradient = create_gradient(size, size, shine_red, metallic_red, 'vertical')
    p_metallic = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    p_metallic.paste(p_gradient, (0, 0))
    
    # Use P shape as mask
    p_alpha = p_layer.split()[-1]
    p_metallic.putalpha(p_alpha)
    
    # Blend P layer
    img = Image.alpha_composite(img, p_metallic)
    
    # Add "EXE" text at bottom with metallic effect
    exe_y = center + 120
    exe_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    exe_draw = ImageDraw.Draw(exe_layer)
    
    # Draw EXE letters as rectangles (simplified)
    letter_width = 40
    letter_height = 60
    letter_spacing = 60
    
    # E
    e_x = center - 90
    exe_draw.rectangle([e_x, exe_y, e_x + letter_width, exe_y + 10], fill=highlight_white)  # Top
    exe_draw.rectangle([e_x, exe_y, e_x + 10, exe_y + letter_height], fill=highlight_white)  # Left
    exe_draw.rectangle([e_x, exe_y + 25, e_x + 30, exe_y + 35], fill=highlight_white)  # Middle
    exe_draw.rectangle([e_x, exe_y + 50, e_x + letter_width, exe_y + letter_height], fill=highlight_white)  # Bottom
    
    # X
    x_x = e_x + letter_spacing
    for i in range(letter_height):
        ratio = i / letter_height
        left_x = int(x_x + ratio * letter_width)
        right_x = int(x_x + letter_width - ratio * letter_width)
        exe_draw.rectangle([left_x, exe_y + i, left_x + 8, exe_y + i + 8], fill=highlight_white)
        exe_draw.rectangle([right_x, exe_y + i, right_x + 8, exe_y + i + 8], fill=highlight_white)
    
    # E (second)
    e2_x = x_x + letter_spacing
    exe_draw.rectangle([e2_x, exe_y, e2_x + letter_width, exe_y + 10], fill=highlight_white)  # Top
    exe_draw.rectangle([e2_x, exe_y, e2_x + 10, exe_y + letter_height], fill=highlight_white)  # Left
    exe_draw.rectangle([e2_x, exe_y + 25, e2_x + 30, exe_y + 35], fill=highlight_white)  # Middle
    exe_draw.rectangle([e2_x, exe_y + 50, e2_x + letter_width, exe_y + letter_height], fill=highlight_white)  # Bottom
    
    # Apply metallic gradient to EXE
    exe_gradient = create_gradient(size, size, highlight_white, shine_red, 'vertical')
    exe_metallic = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    exe_metallic.paste(exe_gradient, (0, 0))
    
    # Use EXE shape as mask
    exe_alpha = exe_layer.split()[-1]
    exe_metallic.putalpha(exe_alpha)
    
    # Blend EXE layer
    img = Image.alpha_composite(img, exe_metallic)
    
    # Add premium shine effects
    # Top highlight
    shine_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shine_draw = ImageDraw.Draw(shine_layer)
    
    # Curved highlight at top
    highlight_radius = base_radius - 120
    shine_draw.arc([center - highlight_radius, center - highlight_radius - 200,
                    center + highlight_radius, center + highlight_radius - 200],
                   -60, 60, width=15, fill=(255, 255, 255, 180))
    
    # Side highlights
    shine_draw.arc([center - base_radius + 50, center - base_radius + 50,
                    center + base_radius - 50, center + base_radius - 50],
                   120, 180, width=8, fill=(255, 200, 200, 120))
    
    shine_draw.arc([center - base_radius + 50, center - base_radius + 50,
                    center + base_radius - 50, center + base_radius - 50],
                   -60, 0, width=8, fill=(255, 200, 200, 120))
    
    # Blend shine effects
    img = Image.alpha_composite(img, shine_layer)
    
    # Apply final enhancements
    # Increase contrast for metallic effect
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    
    # Add subtle sharpening for crisp edges
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    print("✨ Shiny metallic icon created successfully!")
    return img

def create_icns_from_image(image, output_path):
    """Create ICNS file from PIL Image"""
    print("🔧 Creating ICNS file with all required sizes...")
    
    # Create iconset directory
    iconset_dir = output_path.replace('.icns', '.iconset')
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
    
    try:
        # Create all required sizes
        print("📐 Generating all icon sizes...")
        for size, filename in sizes:
            resized = image.resize((size, size), Image.Resampling.LANCZOS)
            icon_path = os.path.join(iconset_dir, filename)
            resized.save(icon_path, 'PNG')
            print(f"   ✓ {filename} ({size}x{size})")
        
        # Convert iconset to icns using macOS iconutil
        print("⚙️  Converting to ICNS format...")
        result = subprocess.run(
            ['iconutil', '-c', 'icns', iconset_dir, '-o', output_path], 
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully created: {output_path}")
            
            # Clean up iconset directory
            subprocess.run(['rm', '-rf', iconset_dir], check=True)
            print("🧹 Cleaned up temporary files")
            
            # Show file info
            size = os.path.getsize(output_path)
            print(f"📊 File size: {size:,} bytes ({size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ iconutil failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating ICNS: {e}")
        return False

def main():
    output_icns = "shiny_red_black.icns"
    preview_png = "shiny_red_black_preview.png"
    
    print("🚀 Shiny Red & Black Icon Creator")
    print("=" * 40)
    
    # Create the shiny icon
    shiny_icon = create_shiny_icon()
    if not shiny_icon:
        return
    
    # Save preview PNG
    shiny_icon.save(preview_png, 'PNG')
    print(f"💾 Saved preview: {preview_png}")
    
    # Create ICNS file
    success = create_icns_from_image(shiny_icon, output_icns)
    
    if success:
        print(f"\n🎉 Shiny icon creation complete!")
        print(f"   Output: {output_icns}")
        print(f"   Preview: {preview_png}")
        print("\n✨ Features:")
        print("   • Premium metallic finish")
        print("   • Red and black color scheme")
        print("   • Professional shine effects")
        print("   • Curved highlights")
        print("   • High contrast metallic text")
        print("   • Retina-ready for all sizes")
    else:
        print(f"\n💥 Icon creation failed!")

if __name__ == '__main__':
    main()
