import tkinter as tk
from tkinter import messagebox
import webbrowser
import pyperclip
import time
import ctypes
import urllib.parse


def ignore_callback_error(*args, **kwargs):
    """Suppress non-critical Tkinter callback exceptions on window close."""
    pass


tk.Tk.report_callback_exception = ignore_callback_error


def get_clipboard_sequence_number():
    """Retrieve the Windows OS clipboard sequence counter via Win32 API."""
    try:
        return ctypes.windll.user32.GetClipboardSequenceNumber()
    except Exception:
        return 0


# Global state storage
history_list = []
is_popup_open = False


def show_custom_popup(address):
    """Display a floating action popup with a 15-second auto-close timer and recent history."""
    global history_list, last_copied_time, last_text, is_popup_open

    is_popup_open = True

    if address in history_list:
        history_list.remove(address)
    history_list.insert(0, address)
    if len(history_list) > 3:
        history_list.pop()

    try:
        root = tk.Tk()
        root.title("SmartClip - Location Assistant")

        window_width = 520
        window_height = 560
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        root.configure(bg="#F8F9FA")
        root.attributes("-topmost", True)
        root.focus_force()
        root.resizable(False, False)

        class AutoCloseTimer:
            _instance = None

            def __init__(self, delay=15000):
                self.delay = delay
                self.job = root.after(self.delay, self.close_window)
                root.bind_all("<Motion>", self.reset_timer)
                root.bind_all("<Key>", self.reset_timer)
                root.bind_all("<Button>", self.reset_timer)
                AutoCloseTimer._instance = self

            def reset_timer(self, event=None):
                try:
                    if self.job:
                        root.after_cancel(self.job)
                    self.job = root.after(self.delay, self.close_window)
                except Exception:
                    pass

            def cancel_timer(self):
                try:
                    if self.job:
                        root.after_cancel(self.job)
                        self.job = None
                except Exception:
                    pass

            def close_window(self):
                global last_copied_time, is_popup_open
                try:
                    if root.winfo_exists():
                        last_copied_time = time.time()
                        is_popup_open = False
                        root.destroy()
                except Exception:
                    pass

        timer_instance = AutoCloseTimer()

        # Header
        header_frame = tk.Frame(root, bg="#2C3E50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        tk.Label(
            header_frame,
            text="📍 SmartClip Location Action Assistant",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg="#2C3E50"
        ).pack(pady=14)

        # Main content container
        content_frame = tk.Frame(root, bg="#F8F9FA", padx=20, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Detected address card
        addr_card = tk.LabelFrame(
            content_frame,
            text=" 🔍 Detected Location ",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )
        addr_card.pack(fill=tk.X, pady=5)

        tk.Label(
            addr_card,
            text=f"📍 {address}",
            font=("Segoe UI", 11, "bold"),
            fg="#E74C3C",
            bg="#FFFFFF",
            wraplength=450,
            justify="left"
        ).pack(side=tk.LEFT, anchor="w", padx=5)

        tk.Label(
            content_frame,
            text="⚡ Select a quick action:",
            font=("Segoe UI", 10, "bold"),
            fg="#7F8C8D",
            bg="#F8F9FA"
        ).pack(anchor="w", pady=(8, 4))

        encoded_address = urllib.parse.quote(address)

        def on_enter(e, hover_bg):
            e.widget["background"] = hover_bg

        def on_leave(e, original_bg):
            e.widget["background"] = original_bg

        def create_styled_button(parent, text, bg_color, hover_color, fg_color, command):
            btn = tk.Button(
                parent,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground=hover_color,
                activeforeground=fg_color,
                bd=0,
                height=2,
                cursor="hand2",
                command=command
            )
            btn.bind("<Enter>", lambda e: on_enter(e, hover_color))
            btn.bind("<Leave>", lambda e: on_leave(e, bg_color))
            return btn

        def click_action(url):
            global last_copied_time, is_popup_open
            timer_instance.cancel_timer()
            last_copied_time = time.time()
            is_popup_open = False
            try:
                root.destroy()
            except Exception:
                pass
            webbrowser.open(url)

        # 1. Google Maps
        btn1 = create_styled_button(
            content_frame,
            "📍  View on Google Maps",
            "#2ECC71", "#27AE60", "#FFFFFF",
            lambda: click_action(f"https://www.google.com/maps/search/?api=1&query={encoded_address}")
        )
        btn1.pack(fill=tk.X, pady=2)

        # 2. Transit & Directions
        btn2 = create_styled_button(
            content_frame,
            "🗺️  Get Directions",
            "#F1C40F", "#D68910", "#191919",
            lambda: click_action(f"https://www.google.com/maps/dir/?api=1&destination={encoded_address}")
        )
        btn2.pack(fill=tk.X, pady=2)

        # 3. Nearby Parking
        btn3 = create_styled_button(
            content_frame,
            "🅿️  Find Nearby Parking",
            "#4A90E2", "#357ABD", "#FFFFFF",
            lambda: click_action(f"https://www.google.com/maps/search/?api=1&query=parking+near+{encoded_address}")
        )
        btn3.pack(fill=tk.X, pady=2)

        # 4. Nearby Restaurants
        btn4 = create_styled_button(
            content_frame,
            "🍴  Explore Nearby Restaurants",
            "#E67E22", "#D35400", "#FFFFFF",
            lambda: click_action(f"https://www.google.com/maps/search/?api=1&query=restaurants+near+{encoded_address}")
        )
        btn4.pack(fill=tk.X, pady=2)

        # 5. Local Weather
        btn5 = create_styled_button(
            content_frame,
            "🌤️  Check Local Weather",
            "#8E44AD", "#7D3C98", "#FFFFFF",
            lambda: click_action(f"https://www.google.com/search?q=weather+{encoded_address}")
        )
        btn5.pack(fill=tk.X, pady=2)

        def make_quick_link(addr):
            def switch_address():
                global last_copied_time, is_popup_open
                timer_instance.cancel_timer()
                last_copied_time = time.time()
                is_popup_open = False
                try:
                    root.destroy()
                except Exception:
                    pass
                show_custom_popup(addr)

            return switch_address

        # Recent history box
        hist_box = tk.LabelFrame(
            content_frame,
            text=" 🕒 Recent Locations ",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#7F8C8D",
            bd=1,
            relief="solid",
            padx=5,
            pady=5
        )
        hist_box.pack(fill=tk.X, pady=(12, 5))

        def clear_history():
            global history_list, last_copied_time, is_popup_open
            if history_list and messagebox.askyesno("Clear History", "Clear all recent location history?"):
                history_list.clear()
                timer_instance.cancel_timer()
                last_copied_time = time.time()
                is_popup_open = False
                try:
                    root.destroy()
                except Exception:
                    pass
                show_custom_popup(address)

        clear_btn = tk.Button(
            hist_box,
            text="[Clear]",
            font=("Segoe UI", 9),
            fg="#95A5A6",
            bg="#FFFFFF",
            activeforeground="#C0392B",
            bd=0,
            cursor="hand2",
            command=clear_history
        )
        clear_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-2, y=-20)

        if history_list:
            for item in history_list:
                display_text = item if len(item) <= 14 else f"{item[:13]}..."
                h_btn = tk.Button(
                    hist_box,
                    text=f"⏱ {display_text}",
                    font=("Segoe UI", 9),
                    bg="#F2F4F4",
                    fg="#34495E",
                    activebackground="#E5E7E9",
                    bd=0,
                    cursor="hand2",
                    command=make_quick_link(item),
                    padx=5,
                    pady=2
                )
                h_btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        else:
            tk.Label(
                hist_box,
                text="No recent history available.",
                font=("Segoe UI", 9, "italic"),
                fg="#BDC3C7",
                bg="#FFFFFF"
            ).pack(pady=2)

        def on_close_window():
            global last_copied_time, is_popup_open
            if AutoCloseTimer._instance:
                AutoCloseTimer._instance.cancel_timer()
            last_copied_time = time.time()
            is_popup_open = False
            try:
                root.destroy()
            except Exception:
                pass

        root.protocol("WM_DELETE_WINDOW", on_close_window)
        root.mainloop()
    except Exception as e:
        print(f"[Error] Failed to render UI: {e}")


def is_location_text(text):
    """Validate whether the copied text matches an address or landmark pattern."""
    lower_text = text.lower()
    landmark_keywords = [
        "빌딩", "타워", "아파트", "병원", "학교", "역", "해변",
        "station", "hospital", "tower", "building", "street", "avenue", "road", "park", "square"
    ]
    if any(kw in lower_text for kw in landmark_keywords):
        return True

    suffixes = ("로", "길", "동", "시", "구", "st", "st.", "ave", "ave.", "rd", "rd.", "blvd")
    for word in lower_text.split():
        cleaned = word.strip(",")
        if cleaned.endswith(suffixes):
            return True

    return False


if __name__ == "__main__":
    print("=" * 60)
    print("SmartClip - Desktop Clipboard & Location Assistant is running.")
    print("Copy any address or landmark (Ctrl+C) to trigger quick actions.")
    print("=" * 60)

    last_text = pyperclip.paste().strip()
    last_copied_time = 0
    last_sequence_num = get_clipboard_sequence_number()

    while True:
        try:
            current_text = pyperclip.paste().strip()
            current_time = time.time()
            current_sequence_num = get_clipboard_sequence_number()

            # Ignore copied source code snippets
            if any(code_token in current_text for code_token in ["import ", "def ", "tk.Tk"]):
                time.sleep(0.5)
                continue

            is_valid_place = is_location_text(current_text)

            if is_valid_place:
                # Prevent duplicate triggers while popup is active
                if is_popup_open:
                    last_sequence_num = current_sequence_num
                    time.sleep(0.5)
                    continue

                time_passed = current_time - last_copied_time

                # Trigger strictly when OS clipboard sequence number increments
                if current_sequence_num != last_sequence_num:
                    last_sequence_num = current_sequence_num

                    # Case 1: Newly copied distinct address
                    if current_text != last_text:
                        last_text = current_text
                        last_copied_time = current_time

                        if len(current_text) <= 60 and current_text.count(" ") <= 6:
                            print(f"[Detected] New location: '{current_text}' -> Launching popup")
                            show_custom_popup(current_text)

                    # Case 2: Re-copied identical address (with 3-second debounce)
                    elif current_text == last_text:
                        if time_passed < 3.0:
                            print("[Ignored] Duplicate copy within 3s cooldown.")
                            continue
                        last_copied_time = current_time
                        print(f"[Re-triggered] Location re-copied: '{current_text}'")
                        show_custom_popup(current_text)

            # Update state when non-location text is copied
            if current_text != last_text and not is_valid_place:
                last_text = current_text
                last_sequence_num = current_sequence_num

            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nSmartClip stopped.")
            break
        except Exception:
            time.sleep(1)
