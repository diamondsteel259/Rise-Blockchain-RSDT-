#!/bin/bash
# RSDT Rebranding Script
# This script replaces all Monero references with RSDT

echo "Starting RSDT rebranding process..."

# Critical files that need immediate rebranding
CRITICAL_FILES=(
    "src/cryptonote_config.h"
    "src/version.h"
    "src/version.cpp.in"
    "README.md"
    "CMakeLists.txt"
)

# Function to replace text in files
replace_text() {
    local file="$1"
    local old_text="$2"
    local new_text="$3"
    
    if [ -f "$file" ]; then
        echo "Updating $file..."
        sed -i "s/$old_text/$new_text/g" "$file"
    fi
}

# Function to replace text case-insensitively
replace_text_case() {
    local file="$1"
    local old_text="$2"
    local new_text="$3"
    
    if [ -f "$file" ]; then
        echo "Updating $file (case-insensitive)..."
        sed -i "s/$old_text/$new_text/gi" "$file"
    fi
}

# Update critical files
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing critical file: $file"
        
        # Replace Monero with RSDT
        replace_text_case "$file" "Monero" "RSDT"
        replace_text_case "$file" "monero" "rsdt"
        replace_text_case "$file" "MONERO" "RSDT"
        
        # Replace specific Monero references
        replace_text "$file" "bitmonero" "rsdt"
        replace_text "$file" "MoneroMessageSignature" "RSDTMessageSignature"
        replace_text "$file" "The Monero Project" "The RSDT Project"
        replace_text "$file" "Monero Project" "RSDT Project"
    fi
done

# Update version information
if [ -f "src/version.cpp.in" ]; then
    echo "Updating version information..."
    replace_text "src/version.cpp.in" "DEF_RSDT_VERSION" "DEF_RSDT_VERSION"
    replace_text "src/version.cpp.in" "DEF_RSDT_RELEASE_NAME" "DEF_RSDT_RELEASE_NAME"
fi

# Update README.md
if [ -f "README.md" ]; then
    echo "Updating README.md..."
    replace_text_case "README.md" "Monero" "RSDT"
    replace_text_case "README.md" "monero" "rsdt"
fi

# Update CMakeLists.txt files
echo "Updating CMakeLists.txt files..."
find . -name "CMakeLists.txt" -exec sed -i 's/monero/rsdt/gi' {} \;

# Update source files
echo "Updating source files..."
find src/ -name "*.cpp" -o -name "*.h" | while read file; do
    if grep -q -i "monero" "$file"; then
        echo "Updating $file..."
        sed -i 's/monero/rsdt/gi' "$file"
    fi
done

# Update Python files
echo "Updating Python files..."
find . -name "*.py" | while read file; do
    if grep -q -i "monero" "$file"; then
        echo "Updating $file..."
        sed -i 's/monero/rsdt/gi' "$file"
    fi
done

# Update documentation files
echo "Updating documentation files..."
find . -name "*.md" -o -name "*.txt" | while read file; do
    if grep -q -i "monero" "$file"; then
        echo "Updating $file..."
        sed -i 's/monero/rsdt/gi' "$file"
    fi
done

echo "Rebranding complete!"
echo "Please review the changes and test the build."

