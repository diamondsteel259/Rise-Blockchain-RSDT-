# RSDT LOGO CHANGE INSTRUCTIONS
## How to Update the RSDT Logo Across All Software Components

---

## 🎨 **CURRENT LOGO DESIGN**

The current RSDT logo is an ASCII art design:

```
██████╗ ███████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██████╔╝███████╗██║  ██║   ██║   
██╔══██╗╚════██║██║  ██║   ██║   
██║  ██║███████║██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   
```

**Design Elements:**
- Professional ASCII art styling
- Clean, modern appearance
- RSDT branding
- Resistance theme integration

---

## 📁 **LOGO FILE LOCATIONS**

### Current Logo Files:
- `/home/daimondsteel259/rsdt/monero/rsdt_logo.svg` - SVG version
- `/home/daimondsteel259/rsdt/monero/rsdt_logo.txt` - ASCII text version

### Software Components Using Logo:
- **Mining Pool**: `rsdt_mining_pool.py` (banner display)
- **Linux Miner**: `rsdt_linux_miner.py` (startup banner)
- **Windows Miner**: `rsdt_windows_miner.cpp` (console output)
- **Android Miner**: `RSDTAndroidMiner.java` (app branding)
- **Blockchain Explorer**: `templates/index.html` (web header)
- **Documentation**: All PDF files (headers)

---

## 🔄 **HOW TO CHANGE THE LOGO**

### Step 1: Create New Logo Design

**Option A: ASCII Art Logo**
1. Create new ASCII art design
2. Save as `rsdt_logo_new.txt`
3. Ensure it fits in console output (max 80 characters wide)

**Option B: SVG Logo**
1. Create new SVG design
2. Save as `rsdt_logo_new.svg`
3. Ensure it's scalable and professional

**Option C: Image Logo**
1. Create PNG/JPG logo (recommended: 512x512px)
2. Save as `rsdt_logo_new.png`
3. Create multiple sizes: 16x16, 32x32, 64x64, 128x128, 256x256, 512x512

### Step 2: Update Logo Files

```bash
# Backup current logo
cp rsdt_logo.txt rsdt_logo_backup.txt
cp rsdt_logo.svg rsdt_logo_backup.svg

# Replace with new logo
cp rsdt_logo_new.txt rsdt_logo.txt
cp rsdt_logo_new.svg rsdt_logo.svg
```

### Step 3: Update Software Components

#### 3.1 Mining Pool (`rsdt_mining_pool.py`)
```python
# Find the banner section and replace:
def print_banner():
    print("""
██████╗ ███████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██████╔╝███████╗██║  ██║   ██║   
██╔══██╗╚════██║██║  ██║   ██║   
██║  ██║███████║██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   

    RESISTANCE BLOCKCHAIN MINING POOL
    Professional Pool Server v1.0
""")
```

#### 3.2 Linux Miner (`rsdt_linux_miner.py`)
```python
# Find the banner section and replace:
def print_banner():
    print("""
██████╗ ███████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██████╔╝███████╗██║  ██║   ██║   
██╔══██╗╚════██║██║  ██║   ██║   
██║  ██║███████║██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   

    RESISTANCE BLOCKCHAIN MINER
    Linux Edition v1.0
""")
```

#### 3.3 Windows Miner (`rsdt_windows_miner.cpp`)
```cpp
// Find the banner section and replace:
void print_banner() {
    std::cout << R"(
██████╗ ███████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██████╔╝███████╗██║  ██║   ██║   
██╔══██╗╚════██║██║  ██║   ██║   
██║  ██║███████║██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   

    RESISTANCE BLOCKCHAIN MINER
    Windows Edition v1.0
)" << std::endl;
}
```

#### 3.4 Android Miner (`RSDTAndroidMiner.java`)
```java
// Update app branding in MainActivity.java
// Change app name, icon, and splash screen
```

#### 3.5 Blockchain Explorer (`templates/index.html`)
```html
<!-- Find the logo section and replace: -->
<div class="logo">
    ██████╗ ███████╗██████╗ ████████╗<br>
    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝<br>
    ██████╔╝███████╗██║  ██║   ██║<br>
    ██╔══██╗╚════██║██║  ██║   ██║<br>
    ██║  ██║███████║██████╔╝   ██║<br>
    ╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝
</div>
```

### Step 4: Update Documentation

#### 4.1 Regenerate PDFs
```bash
# Update all PDF documents with new logo
cd /home/daimondsteel259/rsdt/monero

# Regenerate Tokenomics Paper
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_TOKENOMICS_PAPER.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_TOKENOMICS_PAPER.html

# Regenerate Deployment Bible
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_DEPLOYMENT_BIBLE.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_DEPLOYMENT_BIBLE.md

# Regenerate Overview
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_BLOCKCHAIN_OVERVIEW.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_BLOCKCHAIN_OVERVIEW.md

# Regenerate Whitepaper
google-chrome --headless --disable-gpu --print-to-pdf=RESISTANCE_BLOCKCHAIN_WHITEPAPER.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RESISTANCE_BLOCKCHAIN_WHITEPAPER.html

# Copy to Documents folder
cp *.pdf ~/Documents/
```

### Step 5: Test Logo Changes

#### 5.1 Test Software Components
```bash
# Test mining pool
python3 rsdt_mining_pool.py --help

# Test Linux miner
python3 rsdt_linux_miner.py --help

# Test blockchain explorer
python3 rsdt_blockchain_explorer.py &
curl http://localhost:8080
```

#### 5.2 Verify Logo Display
- Check console output for ASCII art
- Check web interface for logo display
- Check PDF documents for logo headers
- Check Android app for branding

---

## 🎨 **LOGO DESIGN GUIDELINES**

### ASCII Art Requirements:
- **Width**: Maximum 80 characters
- **Height**: 6-8 lines maximum
- **Style**: Professional, clean, readable
- **Characters**: Use box drawing characters (╗╔╚╝║═) for best appearance

### SVG Requirements:
- **Scalable**: Vector format, no pixelation
- **Colors**: Use RSDT brand colors (blue #3498db, dark #2c3e50)
- **Style**: Modern, professional, minimalist
- **Format**: SVG 1.1 compatible

### Image Requirements:
- **Formats**: PNG (transparent), JPG (opaque)
- **Sizes**: 16x16, 32x32, 64x64, 128x128, 256x256, 512x512
- **Quality**: High resolution, professional design
- **Background**: Transparent for PNG, solid color for JPG

---

## 🔧 **AUTOMATION SCRIPT**

Create `update_logo.sh` for automated logo updates:

```bash
#!/bin/bash
# RSDT Logo Update Script

echo "Updating RSDT logo across all components..."

# Backup current logos
cp rsdt_logo.txt rsdt_logo_backup_$(date +%Y%m%d_%H%M%S).txt
cp rsdt_logo.svg rsdt_logo_backup_$(date +%Y%m%d_%H%M%S).svg

# Update logo files
if [ -f "rsdt_logo_new.txt" ]; then
    cp rsdt_logo_new.txt rsdt_logo.txt
    echo "Updated ASCII logo"
fi

if [ -f "rsdt_logo_new.svg" ]; then
    cp rsdt_logo_new.svg rsdt_logo.svg
    echo "Updated SVG logo"
fi

# Regenerate PDFs
echo "Regenerating PDF documents..."
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_TOKENOMICS_PAPER.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_TOKENOMICS_PAPER.html
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_DEPLOYMENT_BIBLE.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_DEPLOYMENT_BIBLE.md
google-chrome --headless --disable-gpu --print-to-pdf=RSDT_BLOCKCHAIN_OVERVIEW.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RSDT_BLOCKCHAIN_OVERVIEW.md
google-chrome --headless --disable-gpu --print-to-pdf=RESISTANCE_BLOCKCHAIN_WHITEPAPER.pdf --print-to-pdf-no-header --virtual-time-budget=5000 file:///home/daimondsteel259/rsdt/monero/RESISTANCE_BLOCKCHAIN_WHITEPAPER.html

# Copy to Documents
cp *.pdf ~/Documents/

echo "Logo update complete!"
echo "Please manually update software components with new logo design."
```

---

## 📋 **CHECKLIST**

- [ ] Create new logo design
- [ ] Backup current logo files
- [ ] Update `rsdt_logo.txt` (ASCII version)
- [ ] Update `rsdt_logo.svg` (SVG version)
- [ ] Update mining pool banner
- [ ] Update Linux miner banner
- [ ] Update Windows miner banner
- [ ] Update Android miner branding
- [ ] Update blockchain explorer logo
- [ ] Regenerate all PDF documents
- [ ] Test all software components
- [ ] Verify logo display across all platforms
- [ ] Update GitHub repositories (when ready)

---

## 🚀 **FINAL NOTES**

1. **Test Thoroughly**: Always test logo changes across all platforms
2. **Backup First**: Always backup current logos before making changes
3. **Consistency**: Ensure logo is consistent across all components
4. **Quality**: Use high-quality designs that represent RSDT professionally
5. **Scalability**: Ensure logo works at different sizes and resolutions

**The logo is a critical part of RSDT's brand identity. Make sure any changes maintain the professional, resistance-focused theme of the project.**

