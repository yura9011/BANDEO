#!/bin/bash
# GSD Universal Installer for Linux/Mac
# Copies GSD framework files to your project directory

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "  GSD Universal Installer (Linux/Mac)"
echo "========================================"
echo ""
echo "This installer will copy GSD framework files to your project."
echo ""

# Get current directory (where GSD is)
GSD_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}GSD Source:${NC} $GSD_SOURCE"
echo ""

# Ask for target directory
while true; do
    read -p "Enter target project directory (full path): " TARGET_DIR
    
    # Validate input
    if [ -z "$TARGET_DIR" ]; then
        echo -e "${RED}[ERROR]${NC} Target directory cannot be empty."
        echo ""
        continue
    fi
    
    # Expand ~ to home directory
    TARGET_DIR="${TARGET_DIR/#\~/$HOME}"
    
    # Check if target exists
    if [ ! -d "$TARGET_DIR" ]; then
        echo ""
        echo -e "${YELLOW}[WARN]${NC} Directory does not exist: $TARGET_DIR"
        read -p "Create it? (y/n): " CREATE
        if [[ "$CREATE" =~ ^[Yy]$ ]]; then
            mkdir -p "$TARGET_DIR" || {
                echo -e "${RED}[ERROR]${NC} Failed to create directory."
                continue
            }
            echo -e "${GREEN}[OK]${NC} Directory created."
        else
            continue
        fi
    fi
    
    break
done

echo ""
echo -e "${BLUE}Target:${NC} $TARGET_DIR"
echo ""

# Confirm installation
read -p "Install GSD to this directory? (y/n): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""
echo "========================================"
echo "  Installing GSD Universal..."
echo "========================================"
echo ""

# Function to copy with confirmation
copy_with_confirm() {
    local source="$1"
    local target="$2"
    local name="$3"
    
    if [ -e "$target" ]; then
        echo -e "${YELLOW}[WARN]${NC} $name already exists in target."
        read -p "Overwrite? (y/n): " OVERWRITE
        if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}[SKIP]${NC} Skipping $name."
            return 1
        fi
    fi
    
    cp -r "$source" "$target"
    return 0
}

# Copy .gsd directory
echo "[1/6] Copying .gsd directory..."
if copy_with_confirm "$GSD_SOURCE/.gsd" "$TARGET_DIR/.gsd" ".gsd directory"; then
    echo -e "${GREEN}[OK]${NC} .gsd directory copied."
fi

# Copy scripts directory
echo "[2/6] Copying scripts directory..."
if copy_with_confirm "$GSD_SOURCE/scripts" "$TARGET_DIR/scripts" "scripts directory"; then
    echo -e "${GREEN}[OK]${NC} scripts directory copied."
fi

# Copy loop scripts
echo "[3/6] Copying loop scripts..."
cp "$GSD_SOURCE/loop.sh" "$TARGET_DIR/loop.sh"
cp "$GSD_SOURCE/loop.ps1" "$TARGET_DIR/loop.ps1"
chmod +x "$TARGET_DIR/loop.sh"
echo -e "${GREEN}[OK]${NC} loop.sh and loop.ps1 copied."

# Copy prompt templates
echo "[4/6] Copying prompt templates..."
cp "$GSD_SOURCE/PROMPT_build.md" "$TARGET_DIR/PROMPT_build.md"
cp "$GSD_SOURCE/PROMPT_plan.md" "$TARGET_DIR/PROMPT_plan.md"
echo -e "${GREEN}[OK]${NC} PROMPT_build.md and PROMPT_plan.md copied."

# Copy AGENTS.md
echo "[5/6] Copying AGENTS.md..."
cp "$GSD_SOURCE/AGENTS.md" "$TARGET_DIR/AGENTS.md"
echo -e "${GREEN}[OK]${NC} AGENTS.md copied."

# Copy documentation (optional)
echo "[6/6] Copying documentation..."
read -p "Copy documentation files (QUICKSTART.md, etc.)? (y/n): " COPY_DOCS
if [[ "$COPY_DOCS" =~ ^[Yy]$ ]]; then
    cp "$GSD_SOURCE/QUICKSTART.md" "$TARGET_DIR/QUICKSTART.md" 2>/dev/null || true
    cp "$GSD_SOURCE/README.md" "$TARGET_DIR/GSD-README.md" 2>/dev/null || true
    echo -e "${GREEN}[OK]${NC} Documentation copied."
else
    echo -e "${YELLOW}[SKIP]${NC} Documentation not copied."
fi

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "GSD Universal has been installed to:"
echo "$TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. cd \"$TARGET_DIR\""
echo "  2. Read QUICKSTART.md for getting started"
echo "  3. Run: ./scripts/validate.sh --all"
echo "  4. Start using GSD!"
echo ""
echo "For existing projects:"
echo "  - Run: ./scripts/index-codebase.sh"
echo "  - Read: .gsd/guides/brownfield.md"
echo ""
