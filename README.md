# SmartClip — Real-Time Windows Clipboard Automation & Text Normalization

A lightweight, zero-dependency Windows background utility built in Python that monitors system clipboard events in real time, automatically sanitizes and normalizes copied text, and dispatches non-intrusive system notifications.

## Key Engineering Features
- **Low-Overhead Win32 API Polling (`ctypes`):** Interfaces directly with native Windows user32/kernel32 APIs (`OpenClipboard`, `GetClipboardData`, `GlobalLock`) without heavy third-party GUI frameworks.
- **Self-Trigger Debounce Control (`3.0s`):** Implements a deterministic cooldown state machine to prevent infinite polling loops when programmatic clipboard re-writes occur.
- **Encoding-Safe Text Normalization:** Automatically trims trailing whitespace, collapses redundant line breaks, and strips formatting artifacts with strict `UTF-16LE` / `UTF-8` memory buffer handling to eliminate `UnicodeDecodeError` crashes.

## Tech Stack
- **Language:** Python 3.x
- **System Interface:** Windows Win32 API (`ctypes`), `win10toast` / native notification dispatch
- **Architecture:** Event-driven background daemon with minimal CPU/RAM footprint

## Usage
```bash
python smartclip.py
