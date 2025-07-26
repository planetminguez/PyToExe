#!/bin/bash

# Python2Exe DMG Creation Script
# Creates an attractive DMG with custom red/black icon

set -e

# Configuration
APP_NAME="Python2Exe"
DMG_NAME="Python2Exe-v5.0-DebugFixed"
SOURCE_APP="/Users/minguez/Desktop/Python2Exe.app"
DMG_DIR="/Users/minguez/Desktop/Python2Exe-DMG"
RESOURCES_DIR="$DMG_DIR/Resources"
TEMP_DMG="$DMG_DIR/temp.dmg"
FINAL_DMG="/Users/minguez/Desktop/$DMG_NAME.dmg"

echo "🚀 Creating Python2Exe DMG..."

# Check if source app exists
if [ ! -d "$SOURCE_APP" ]; then
    echo "❌ Error: Python2Exe.app not found at $SOURCE_APP"
    exit 1
fi

# Create temporary directory for DMG contents
TEMP_DIR="$DMG_DIR/dmg_temp"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy the app to temp directory and rename it
echo "📦 Copying Python2Exe.app..."
cp -R "$SOURCE_APP" "$TEMP_DIR/Python2Exe.app"

# Create Applications symlink
echo "🔗 Creating Applications symlink..."
ln -s /Applications "$TEMP_DIR/Applications"

# Use pre-created shiny background
echo "🌟 Using shiny metallic background..."

# Create temporary DMG
echo "💾 Creating temporary DMG..."
rm -f "$TEMP_DMG"
hdiutil create -srcfolder "$TEMP_DIR" -volname "$APP_NAME" -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" -format UDRW -size 100m "$TEMP_DMG"

# Mount the temporary DMG
echo "🔧 Mounting and configuring DMG..."
MOUNT_DIR="/Volumes/$APP_NAME"
hdiutil attach "$TEMP_DMG" -readwrite -mount required

# Wait for mount
sleep 2

# Apply custom icon to the DMG volume
if [ -f "$RESOURCES_DIR/Python2Exe.icns" ]; then
    echo "🎯 Applying custom icon to DMG..."
    cp "$RESOURCES_DIR/Python2Exe.icns" "$MOUNT_DIR/.VolumeIcon.icns"
    SetFile -c icnC "$MOUNT_DIR/.VolumeIcon.icns"
    SetFile -a C "$MOUNT_DIR"
fi

# Apply custom icon to the app
if [ -f "$RESOURCES_DIR/Python2Exe.icns" ]; then
    echo "🎯 Applying custom icon to app..."
    mkdir -p "$MOUNT_DIR/Python2Exe.app/Contents/Resources"
    cp "$RESOURCES_DIR/Python2Exe.icns" "$MOUNT_DIR/Python2Exe.app/Contents/Resources/AppIcon.icns"
    # Update Info.plist to reference the new icon
    /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile AppIcon" "$MOUNT_DIR/Python2Exe.app/Contents/Info.plist" 2>/dev/null || true
fi

# Set background and configure Finder view
echo "🖼️  Configuring Finder view..."
if [ -f "$RESOURCES_DIR/dmg_background.png" ]; then
    mkdir -p "$MOUNT_DIR/.background"
    cp "$RESOURCES_DIR/dmg_background.png" "$MOUNT_DIR/.background/background.png"
fi

# Configure Finder view with AppleScript
osascript <<EOF
tell application "Finder"
    tell disk "$APP_NAME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {100, 100, 700, 500}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 128
        set background picture of viewOptions to file ".background:background.png"
        
        -- Position icons
        set position of item "Python2Exe.app" of container window to {150, 200}
        set position of item "Applications" of container window to {450, 200}
        
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
EOF

# Ensure changes are written
sync
sleep 2

# Unmount the DMG
echo "📤 Finalizing DMG..."
hdiutil detach "$MOUNT_DIR"

# Convert to compressed, read-only DMG
echo "🗜️  Compressing DMG..."
rm -f "$FINAL_DMG"
hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$FINAL_DMG"

# Clean up
rm -f "$TEMP_DMG"
rm -rf "$TEMP_DIR"

# Set custom icon on final DMG
if [ -f "$RESOURCES_DIR/Python2Exe.icns" ]; then
    echo "🎯 Setting final DMG icon..."
    sips -i "$RESOURCES_DIR/Python2Exe.icns" "$FINAL_DMG" >/dev/null 2>&1 || true
    DeRez -only icns "$RESOURCES_DIR/Python2Exe.icns" > /tmp/icon.rsrc 2>/dev/null || true
    Rez -append /tmp/icon.rsrc -o "$FINAL_DMG" 2>/dev/null || true
    SetFile -a C "$FINAL_DMG" 2>/dev/null || true
    rm -f /tmp/icon.rsrc 2>/dev/null || true
fi

echo "✅ DMG created successfully: $FINAL_DMG"
echo "📊 DMG Size: $(du -h "$FINAL_DMG" | cut -f1)"
echo ""
echo "🎉 Your Python2Exe DMG is ready!"
echo "   • Shiny metallic red & black icon"
echo "   • Premium metallic background"
echo "   • Drag-to-install interface"
echo "   • Professional presentation"
echo "   • Diagonal shine effects"
echo "   • 3D text with glow"
