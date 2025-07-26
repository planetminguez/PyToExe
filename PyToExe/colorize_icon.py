#!/usr/bin/env python3
"""
Convert existing ICNS icon to attractive red and black color scheme
"""

import os
import subprocess
import tempfile
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

def extract_largest_icon(icns_path):
    """Extract the largest icon from ICNS file"""
    print(f"📤 Extracting icon from {icns_path}...")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Use sips to extract the largest size (1024x1024)
        extracted_path = os.path.join(temp_dir, "extracted.png")
        result = subprocess.run([
            'sips', '-s', 'format', 'png', 
            icns_path, '--out', extracted_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(extracted_path):
            return extracted_path
        else:
            print(f"❌ Failed to extract icon: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error extracting icon: {e}")
        return None

def create_red_black_version(image_path):
    """Transform image to attractive red and black color scheme"""
    print("🎨 Applying red and black color transformation...")
    
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Convert to numpy array for advanced processing
        img_array = np.array(img)
        
        # Separate alpha channel
        alpha = img_array[:, :, 3]
        rgb = img_array[:, :, :3]
        
        # Convert to grayscale to get luminance values
        gray = np.dot(rgb, [0.299, 0.587, 0.114])
        
        # Create red and black color mapping based on luminance
        # Dark areas -> Black, Light areas -> Red, Mid areas -> Dark Red
        red_channel = np.zeros_like(gray)
        green_channel = np.zeros_like(gray)
        blue_channel = np.zeros_like(gray)
        
        # Define color zones based on luminance
        # Very dark (0-60): Pure black
        dark_mask = gray < 60
        red_channel[dark_mask] = 0
        green_channel[dark_mask] = 0
        blue_channel[dark_mask] = 0
        
        # Dark-medium (60-120): Dark red
        dark_mid_mask = (gray >= 60) & (gray < 120)
        red_channel[dark_mid_mask] = 80
        green_channel[dark_mid_mask] = 0
        blue_channel[dark_mid_mask] = 0
        
        # Medium (120-180): Medium red
        mid_mask = (gray >= 120) & (gray < 180)
        red_channel[mid_mask] = 160
        green_channel[mid_mask] = 20
        blue_channel[mid_mask] = 20
        
        # Light-medium (180-220): Bright red
        light_mid_mask = (gray >= 180) & (gray < 220)
        red_channel[light_mid_mask] = 220
        green_channel[light_mid_mask] = 40
        blue_channel[light_mid_mask] = 40
        
        # Light (220+): Crimson red
        light_mask = gray >= 220
        red_channel[light_mask] = 255
        green_channel[light_mask] = 60
        blue_channel[light_mask] = 60
        
        # Combine channels
        new_rgb = np.stack([red_channel, green_channel, blue_channel], axis=2)
        new_rgba = np.concatenate([new_rgb, alpha[:, :, np.newaxis]], axis=2)
        
        # Convert back to PIL Image
        new_img = Image.fromarray(new_rgba.astype(np.uint8), 'RGBA')
        
        # Apply some post-processing for better visual appeal
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(new_img)
        new_img = enhancer.enhance(1.2)
        
        # Add subtle sharpening
        new_img = new_img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        print("✨ Applied red and black color transformation")
        return new_img
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None

def create_icns_from_image(image, output_path):
    """Create ICNS file from PIL Image"""
    print("🔧 Creating new ICNS file...")
    
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
    input_icns = "icon.icns"
    output_icns = "icon_red_black.icns"
    
    print("🚀 Red & Black Icon Converter")
    print("=" * 35)
    
    if not os.path.exists(input_icns):
        print(f"❌ Error: {input_icns} not found")
        return
    
    # Step 1: Extract the largest icon
    extracted_path = extract_largest_icon(input_icns)
    if not extracted_path:
        return
    
    # Step 2: Apply red and black color transformation
    red_black_image = create_red_black_version(extracted_path)
    if not red_black_image:
        return
    
    # Step 3: Create new ICNS file
    success = create_icns_from_image(red_black_image, output_icns)
    
    # Clean up extracted file
    try:
        os.remove(extracted_path)
        os.rmdir(os.path.dirname(extracted_path))
    except:
        pass
    
    if success:
        print(f"\n🎉 Conversion complete!")
        print(f"   Input:  {input_icns}")
        print(f"   Output: {output_icns}")
        print("\n🎨 Color Scheme Applied:")
        print("   • Dark areas → Pure black")
        print("   • Shadow areas → Dark red")
        print("   • Mid-tones → Medium red") 
        print("   • Highlights → Bright red")
        print("   • Light areas → Crimson red")
        print("\n✨ Enhanced with:")
        print("   • Improved contrast")
        print("   • Subtle sharpening")
        print("   • Professional finish")
    else:
        print(f"\n💥 Conversion failed!")

if __name__ == '__main__':
    main()
