"""
Screen Text Monitor and Screenshot Tool

This script monitors a selected screen region for specified text using OCR (Optical Character Recognition).
When the specified text is found, it automatically captures full screen screenshots.
Originally created to monitor the NPO Radio 2 Top 2000 broadcast for specific artist names.

Author: Youp Verkooijen
Copyright (C) 2024 Youp Verkooijen
License: GNU Affero General Public License v3.0
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Any use, modification, or distribution of this software must retain
the attribution: "Originally created by Youp Verkooijen (2024)"
"""

import pyautogui
import tkinter as tk
from PIL import Image, ImageGrab
import pytesseract
import time
from datetime import datetime
import os

# Configuration Constants
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
SCREENSHOT_FOLDER = "screenshots"
CHECK_INTERVAL = 2.5  # Time in seconds between each check
SCREENSHOT_INTERVAL = 1.0  # Time in seconds between screenshots when text is detected
SELECTOR_WINDOW_OPACITY = 0.3  # Transparency of the region selector window
SELECTION_RECTANGLE_COLOR = 'red'
SELECTION_RECTANGLE_WIDTH = 2

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class RegionSelector:
    """
    A class to create a fullscreen transparent window that allows users to select
    a screen region by clicking and dragging.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', SELECTOR_WINDOW_OPACITY)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.region = None
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Bind Escape key to quit
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
    def on_click(self, event):
        """Handle mouse click event to start region selection."""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
            
    def on_drag(self, event):
        """Handle mouse drag event to update the visual selection rectangle."""
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline=SELECTION_RECTANGLE_COLOR,
            width=SELECTION_RECTANGLE_WIDTH
        )
        
    def on_release(self, event):
        """Handle mouse release event to finalize the region selection."""
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.region = (x1, y1, x2, y2)
        self.root.quit()
        
    def get_region(self):
        """Start the region selection process and return the selected region."""
        self.root.mainloop()
        self.root.destroy()
        return self.region

def capture_and_check_region(region, target_names):
    """
    Capture a screenshot of the specified region and check for target names using OCR.
    
    Args:
        region (tuple): The region coordinates (x1, y1, x2, y2)
        target_names (list): List of names to search for in the region
        
    Returns:
        tuple: (bool, str) - (Whether a name was found, The name that was found)
    """
    screenshot = ImageGrab.grab(bbox=region)
    text = pytesseract.image_to_string(screenshot)
    
    for name in target_names:
        if name in text:
            return True, name
    return False, None

def save_full_screenshot(detected_name):
    """
    Save a full screenshot with timestamp and detected name in the filename.
    
    Args:
        detected_name (str): The name that was detected in the region
    """
    if not os.path.exists(SCREENSHOT_FOLDER):
        os.makedirs(SCREENSHOT_FOLDER)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot = ImageGrab.grab()
    screenshot.save(f'{SCREENSHOT_FOLDER}/screenshot_{detected_name}_{timestamp}.png')

def get_target_names():
    """
    Prompt the user to enter names to monitor for.
    
    Returns:
        list: List of names to monitor for
    """
    names = []
    print("Enter the names to look for (one per line). Press Enter twice when done:")
    while True:
        name = input().strip()
        if not name:  # Empty line
            if names:  # If we have at least one name
                break
            print("Please enter at least one name:")
            continue
        names.append(name)
    return names

def main():
    """Main function to run the screen monitoring and screenshot tool."""
    # Get the list of names to search for
    target_names = get_target_names()
    print(f"\nWill look for these names: {', '.join(target_names)}")
    
    print("\nSelect the region to monitor (Click and drag, press ESC to cancel)")
    selector = RegionSelector()
    region = selector.get_region()
    
    if not region:
        print("No region selected. Exiting...")
        return
    
    print(f"Monitoring region {region} for the specified names...")
    print("Press Ctrl+C to stop the script")
    
    try:
        while True:
            found, detected_name = capture_and_check_region(region, target_names)
            if found:
                print(f"'{detected_name}' detected! Taking screenshots...")
                while capture_and_check_region(region, [detected_name])[0]:
                    save_full_screenshot(detected_name)
                    time.sleep(SCREENSHOT_INTERVAL)
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("\nScript stopped by user")

if __name__ == "__main__":
    main()
