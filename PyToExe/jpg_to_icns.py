#!/usr/bin/env python3
"""
Convert JPG to ICNS file for macOS apps
"""

import os
import subprocess
from PIL import Image

def convert_jpg_to_icns(jpg_path, icns_path):
    """Convert JPG to ICNS using PIL and iconutil"""
    
    if not os.path.exists(jpg_path):
        print(f"❌ Error: {jpg_path} not found")
        return False
    
    print(f"🔄 Converting {jpg_path} to ICNS...")
    
    # Create iconset directory
    iconset_dir = icns_path.replace('.icns', '.iconset')
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
        # Load and process the original image
        print("📸 Loading and processing image...")
        original = Image.open(jpg_path)
        
        # Convert to RGBA if not already
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        
        # Make it square by cropping to center if needed
        width, height = original.size
        if width != height:
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            original = original.crop((left, top, right, bottom))
            print(f"🔲 Cropped to square: {size}x{size}")
        
        # Create all required sizes
        print("🎨 Generating icon sizes...")
        for size, filename in sizes:
            resized = original.resize((size, size), Image.Resampling.LANCZOS)
            icon_path = os.path.join(iconset_dir, filename)
            resized.save(icon_path, 'PNG')
            print(f"   ✓ {filename} ({size}x{size})")
        
        # Convert iconset to icns using macOS iconutil
        print("🔧 Converting to ICNS...")
        result = subprocess.run(
            ['iconutil', '-c', 'icns', iconset_dir, '-o', icns_path], 
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully created: {icns_path}")
            
            # Clean up iconset directory
            subprocess.run(['rm', '-rf', iconset_dir], check=True)
            print("🧹 Cleaned up temporary files")
            
            # Show file info
            size = os.path.getsize(icns_path)
            print(f"📊 File size: {size:,} bytes ({size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ iconutil failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False

def main():
    jpg_file = "icon.jpg"
    icns_file = "icon.icns"
    
    print("🚀 JPG to ICNS Converter")
    print("=" * 30)
    
    success = convert_jpg_to_icns(jpg_file, icns_file)
    
    if success:
        print(f"\n🎉 Conversion complete!")
        print(f"   Input:  {jpg_file}")
        print(f"   Output: {icns_file}")
        print("\n💡 You can now use this ICNS file for:")
        print("   • macOS app icons")
        print("   • DMG volume icons") 
        print("   • Dock icons")
    else:
        print(f"\n💥 Conversion failed!")

if __name__ == '__main__':
    main()
