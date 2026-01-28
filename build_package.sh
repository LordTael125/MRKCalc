#!/bin/bash
set -e

# Configuration
APP_NAME="MRKCalc"
DIST_DIR="dist"
APP_DIR="AppDir"
APP_IMAGE_TOOL="appimagetool-x86_64.AppImage"

# 1. Clean previous builds
echo "Cleaning up..."
rm -rf "$DIST_DIR" "$APP_DIR" build *.spec

# 2. Run PyInstaller
echo "Running PyInstaller..."
# We use --add-data to include the GUI folder content into the 'GUI' folder inside the executable
pyinstaller "main.py" \
    --name "$APP_NAME" \
    --onefile \
    --noconsole \
    --add-data "GUI/main.ui:GUI" \
    --clean

# 3. Create AppDir structure
echo "Creating AppDir structure..."
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APP_DIR/usr/share/applications"

# Copy executable
cp "$DIST_DIR/$APP_NAME" "$APP_DIR/usr/bin/$APP_NAME"

# Create helper desktop file
cat > "$APP_DIR/usr/share/applications/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=MRKCalc
Exec=$APP_NAME
Icon=calculator
Categories=Utility;Education;
Terminal=false
EOF

# Create AppRun (symlink to executable for simplicity in this case, or standard AppRun)
# Ideally AppImage uses a standard AppRun, but for onefile binaries we can just link or script it.
# We'll use a simple script as AppRun
cat > "$APP_DIR/AppRun" <<EOF
#!/bin/bash
SELF=\$(readlink -f "\$0")
HERE=\${SELF%/*}
export PATH="\${HERE}/usr/bin:\${PATH}"
export LD_LIBRARY_PATH="\${HERE}/usr/lib:\${LD_LIBRARY_PATH}"
exec "$APP_NAME" "\$@"
EOF
chmod +x "$APP_DIR/AppRun"

# Add a dummy icon if none exists (required for AppImage)
# Uses a generic calculator icon if available or creates a placeholder
if [ ! -f "icon.png" ]; then
    # Create simple solid color png using python if valid icon not found
    python3 -c "from PyQt5 import QtGui; i = QtGui.QImage(256, 256, QtGui.QImage.Format_ARGB32); i.fill(QtGui.QColor('teal')); i.save('icon.png')"
fi
cp icon.png "$APP_DIR/usr/share/icons/hicolor/256x256/apps/calculator.png"
cp icon.png "$APP_DIR/.DirIcon"
cp icon.png "$APP_DIR/calculator.png"
cp "$APP_DIR/usr/share/applications/$APP_NAME.desktop" "$APP_DIR/"

# 4. Download appimagetool if not present
if [ ! -f "$APP_IMAGE_TOOL" ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x "$APP_IMAGE_TOOL"
fi

# 5. Build AppImage
echo "Building AppImage..."
./"$APP_IMAGE_TOOL" "$APP_DIR" "$APP_NAME.AppImage"

echo "Done! Created $APP_NAME.AppImage"
