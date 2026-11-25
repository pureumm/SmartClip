# SmartClip — Windows Clipboard Location Action Assistant

A lightweight Windows desktop utility built in Python that monitors OS clipboard events in real time, detects copied addresses or landmarks, and launches an instant floating Tkinter action assistant for Google Maps navigation, nearby parking, restaurants, and local weather.

## Key Engineering Features
- **OS-Level Event Detection (`GetClipboardSequenceNumber`):** Polls the native Windows `user32` clipboard sequence counter via `ctypes` rather than blindly reading text, minimizing CPU overhead and preventing redundant UI triggers.
- **Bilingual Location Heuristic Engine (`is_location_text`):** Automatically identifies Korean and English addresses/landmarks (e.g., `-로`, `-길`, `-동`, `Street`, `Avenue`, `Station`, `Tower`) while filtering out source code snippets (`import`, `def`, `tk.Tk`).
- **Debounce & State Management (`3.0s` Cooldown):** Implements duplicate-copy cooldown protection, modal lock (`is_popup_open`), and a 15-second inactivity auto-close timer (`AutoCloseTimer`) that resets dynamically on mouse or keyboard interaction.
- **One-Click Location Workflows & History:** Provides instant URL-encoded deep links to Google Maps, Directions, Nearby Parking, Restaurants, and Weather, alongside an interactive 3-item recent location switcher.

## Tech Stack
- **Language:** Python 3.x
- **GUI & OS Integration:** `tkinter`, Windows Win32 API (`ctypes.windll.user32`), `pyperclip`, `webbrowser`, `urllib.parse`

## Usage
```bash
pip install pyperclip
python smartclip.py
