#!/bin/bash

# 📦 Download config
RAW_URL="https://raw.githubusercontent.com/Sulfate-D/Mac-Spoofer/main/main.py"
SCRIPT_NAME="macspoof"
INSTALL_DIR="$HOME/.macspoof"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
LINK_PATH="/usr/local/bin/$SCRIPT_NAME"

echo "📥 Installing $SCRIPT_NAME from:"
echo "$RAW_URL"
echo

# 📁 Create install directory
mkdir -p "$INSTALL_DIR"

# ⬇️ Download script
curl -sSL "$RAW_URL" -o "$SCRIPT_PATH"

# ➕ Add shebang if missing
if ! head -1 "$SCRIPT_PATH" | grep -q '#!/usr/bin/env python3'; then
  echo "⚙️ Adding shebang..."
  echo -e "#!/usr/bin/env python3\n$(cat "$SCRIPT_PATH")" > "$SCRIPT_PATH"
fi

# 🔒 Make it executable
chmod +x "$SCRIPT_PATH"

# 🔗 Link it to /usr/local/bin
echo "🔗 Creating symlink at $LINK_PATH..."
sudo ln -sf "$SCRIPT_PATH" "$LINK_PATH"

echo
echo "✅ Done! You can now run:"
echo "    $SCRIPT_NAME"
echo
echo "🚀 This will launch your tkinter GUI instantly!"
