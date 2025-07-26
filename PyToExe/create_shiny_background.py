#!/usr/bin/env python3
"""
Create a shiny red and black DMG background image with metallic effects
"""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
import math
import numpy as np

def create_metallic_gradient(width, height, color1, color2, direction='vertical'):
    """Create a metallic gradient with shine bands"""
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            # Add metallic shine bands
            shine_factor = 1.0 + 0.3 * math.sin(ratio * math.pi * 8)
            
            r = int((color1[0] * (1 - ratio) + color2[0] * ratio) * shine_factor)
            g = int((color1[1] * (1 - ratio) + color2[1] * ratio) * shine_factor)
            b = int((color1[2] * (1 - ratio) + color2[2] * ratio) * shine_factor)
            
            # Clamp values
            r = min(255, max(0, r))
            g = min(255, max(0, g))
            b = min(255, max(0, b))
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            # Add metallic shine bands
            shine_factor = 1.0 + 0.2 * math.sin(ratio * math.pi * 6)
            
            r = int((color1[0] * (1 - ratio) + color2[0] * ratio) * shine_factor)
            g = int((color1[1] * (1 - ratio) + color2[1] * ratio) * shine_factor)
            b = int((color1[2] * (1 - ratio) + color2[2] * ratio) * shine_factor)
            
            # Clamp values
            r = min(255, max(0, r))
            g = min(255, max(0, g))
            b = min(255, max(0, b))
            
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    
    return gradient

def create_radial_shine(width, height, center, max_radius, inner_color, outer_color):
    """Create a radial shine effect"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        for x in range(width):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            if distance <= max_radius:
                ratio = distance / max_radius
                # Add pulsing shine effect
                shine_factor = 1.0 + 0.4 * math.sin(ratio * math.pi * 4)
                
                r = int((inner_color[0] * (1 - ratio) + outer_color[0] * ratio) * shine_factor)
                g = int((inner_color[1] * (1 - ratio) + outer_color[1] * ratio) * shine_factor)
                b = int((inner_color[2] * (1 - ratio) + outer_color[2] * ratio) * shine_factor)
                
                # Clamp values
                r = min(255, max(0, r))
                g = min(255, max(0, g))
                b = min(255, max(0, b))
                
                draw.point((x, y), (r, g, b))
            else:
                draw.point((x, y), outer_color)
    
    return img

def create_shiny_dmg_background():
    """Create a premium shiny DMG background"""
    print("🌟 Creating shiny DMG background...")
    
    width, height = 600, 400
    
    # Define premium metallic colors
    deep_black = (8, 8, 8)
    metallic_black = (25, 25, 25)
    dark_red = (80, 15, 15)
    metallic_red = (150, 25, 25)
    bright_red = (200, 40, 40)
    shine_red = (255, 80, 80)
    
    # Create base metallic gradient
    base_gradient = create_metallic_gradient(width, height, metallic_black, deep_black, 'vertical')
    
    # Create radial shine overlay
    center_x, center_y = width // 2, height // 2 - 50
    radial_shine = create_radial_shine(width, height, (center_x, center_y), 
                                     min(width, height) // 2, bright_red, dark_red)
    
    # Blend the gradients
    bg = Image.blend(base_gradient, radial_shine, 0.6)
    
    # Add metallic horizontal stripes for premium effect
    draw = ImageDraw.Draw(bg)
    
    # Add thin metallic stripes
    stripe_spacing = 40
    for y in range(0, height, stripe_spacing):
        stripe_intensity = int(40 + 20 * math.sin(y / 50))
        stripe_color = (stripe_intensity, stripe_intensity // 4, stripe_intensity // 4)
        draw.line([(0, y), (width, y)], fill=stripe_color)
        draw.line([(0, y + 1), (width, y + 1)], fill=(stripe_intensity // 2, 0, 0))
    
    # Add central red metallic band
    band_height = 80
    band_y = height // 2 - band_height // 2
    
    # Create metallic band gradient
    band_gradient = create_metallic_gradient(width, band_height, shine_red, dark_red, 'vertical')
    
    # Create shine overlay for the band
    band_shine = Image.new('RGB', (width, band_height))
    band_draw = ImageDraw.Draw(band_shine)
    
    for x in range(width):
        shine_intensity = int(100 + 60 * math.sin(x / 30))
        shine_color = (min(255, shine_intensity), min(255, shine_intensity // 3), min(255, shine_intensity // 3))
        band_draw.line([(x, 0), (x, band_height)], fill=shine_color)
    
    # Blend band with shine
    shiny_band = Image.blend(band_gradient, band_shine, 0.4)
    
    # Paste the shiny band onto background with transparency
    bg.paste(shiny_band, (0, band_y))
    
    # Add premium text with metallic effect
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 52)
        subtitle_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Create text layer for proper blending
    text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    
    # Main title with metallic effect
    title = 'Python2Exe'
    title_bbox = text_draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 40
    
    # Create multiple text layers for metallic effect
    # Shadow layer (deep)
    for offset in [4, 3, 2]:
        text_draw.text((title_x + offset, title_y + offset), title, 
                      font=title_font, fill=(20, 5, 5, 200))
    
    # Metallic base layer
    text_draw.text((title_x, title_y), title, font=title_font, fill=(180, 50, 50, 255))
    
    # Highlight layer
    text_draw.text((title_x - 1, title_y - 1), title, font=title_font, fill=(255, 120, 120, 200))
    
    # Top shine
    text_draw.text((title_x - 2, title_y - 2), title, font=title_font, fill=(255, 200, 200, 150))
    
    # Subtitle with glow effect
    subtitle = 'Drag to Applications to Install'
    sub_bbox = text_draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = height - 70
    
    # Glow effect for subtitle
    for offset in [3, 2, 1]:
        glow_alpha = int(100 - offset * 30)
        text_draw.text((sub_x + offset, sub_y + offset), subtitle, 
                      font=subtitle_font, fill=(100, 20, 20, glow_alpha))
        text_draw.text((sub_x - offset, sub_y - offset), subtitle, 
                      font=subtitle_font, fill=(100, 20, 20, glow_alpha))
    
    # Main subtitle text
    text_draw.text((sub_x, sub_y), subtitle, font=subtitle_font, fill=(220, 220, 220, 255))
    
    # Blend text layer with background
    bg = bg.convert('RGBA')
    bg = Image.alpha_composite(bg, text_layer)
    bg = bg.convert('RGB')
    
    # Add final metallic shine effects
    # Diagonal shine streaks
    shine_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shine_draw = ImageDraw.Draw(shine_layer)
    
    # Multiple diagonal shine lines
    for i in range(0, width + height, 60):
        x1, y1 = i - height, 0
        x2, y2 = i, height
        
        # Create shine gradient along the line
        for offset in range(5):
            alpha = int(80 - offset * 15)
            shine_draw.line([(x1 + offset, y1), (x2 + offset, y2)], 
                          fill=(255, 150, 150, alpha), width=2)
    
    # Blend shine effects
    bg = bg.convert('RGBA')
    bg = Image.alpha_composite(bg, shine_layer)
    bg = bg.convert('RGB')
    
    # Apply final enhancements
    # Increase contrast for metallic effect
    enhancer = ImageEnhance.Contrast(bg)
    bg = enhancer.enhance(1.2)
    
    # Add slight blur for smooth metallic finish
    bg = bg.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Final sharpening for crisp text
    bg = bg.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
    
    print("✨ Shiny DMG background created successfully!")
    return bg

def main():
    output_file = "shiny_dmg_background.png"
    
    print("🚀 Shiny DMG Background Creator")
    print("=" * 35)
    
    # Create the shiny background
    shiny_bg = create_shiny_dmg_background()
    
    if shiny_bg:
        # Save the background
        shiny_bg.save(output_file, 'PNG')
        print(f"💾 Saved: {output_file}")
        
        # Show file info
        size = os.path.getsize(output_file)
        print(f"📊 File size: {size:,} bytes ({size/1024:.1f} KB)")
        
        print(f"\n🎉 Shiny background creation complete!")
        print(f"   Output: {output_file}")
        print("\n✨ Features:")
        print("   • Premium metallic finish")
        print("   • Red and black gradient")
        print("   • Metallic stripe patterns")
        print("   • Diagonal shine effects")
        print("   • 3D text with glow")
        print("   • Professional DMG presentation")
    else:
        print(f"\n💥 Background creation failed!")

if __name__ == '__main__':
    import os
    main()
