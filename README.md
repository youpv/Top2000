# Top 2000 Screen Monitor

A Python script that monitors a selected screen region for specific text and automatically captures screenshots when the text is detected. Originally created to monitor the NPO Radio 2 Top 2000 broadcast for specific message senders, but can be used for any text monitoring purpose.

Copyright (C) 2024 Youp Verkooijen. All rights reserved.

## Features

- Visual region selection for monitoring
- Real-time OCR text detection
- Multiple name monitoring
- Automatic full-screen screenshots when text is detected
- Timestamped screenshot saving
- Easy to configure timing parameters

## Prerequisites

1. Python 3.6 or higher
2. Tesseract OCR installed on your system
   - Windows: Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Make sure to note the installation path (default: `C:\Program Files\Tesseract-OCR\tesseract.exe`)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/youpv/Top2000-Message-Monitor
cd top2000-monitor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install pyautogui pillow pytesseract
```

## Configuration

You can adjust the following constants in `main.py` to customize the behavior:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path
SCREENSHOT_FOLDER = "screenshots"  # Folder where screenshots will be saved
CHECK_INTERVAL = 2.5  # Time in seconds between each check
SCREENSHOT_INTERVAL = 1.0  # Time in seconds between screenshots when text is detected
```

## Usage

1. Run the script:
```bash
python main.py
```

2. Enter the names you want to monitor for:
   - Type each name on a new line
   - Press Enter twice when done
   - Example:
     ```
     Enter the names to look for (one per line). Press Enter twice when done:
     Youp
     Queen
     Michael Jackson
     [Enter]
     [Enter]
     ```

3. Select the screen region to monitor:
   - A semi-transparent window will appear
   - Click and drag to select the region where the text should appear
   - Press ESC to cancel the selection

4. The script will start monitoring:
   - It checks the selected region every 2.5 seconds
   - When a monitored name is found, it takes screenshots every second
   - Screenshots are saved in the `screenshots` folder
   - Press Ctrl+C to stop the script

## Screenshot Naming

Screenshots are saved with the following format:
```
screenshots/screenshot_[detected_name]_[YYYYMMDD_HHMMSS].png
```

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Important licensing notes:
- Any use, modification, or distribution must retain the original attribution
- Modified versions must be clearly marked as such
- Network use constitutes distribution
- Complete source code must be made available
- The original author (Youp Verkooijen) must be credited in all derivative works

For more details about your rights and obligations under this license, please see the LICENSE file.

## Attribution

Originally created by Youp Verkooijen (2024)

## Contributing

Contributions are welcome, but please note:
1. All contributions must comply with the AGPL-3.0 license
2. You must agree to license your contributions under the same license
3. You must add appropriate attribution notices
4. Please open an issue first to discuss major changes 