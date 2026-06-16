import random
import tkinter as tk
import win32con
import win32gui


class TransparentOverlay:

    def __init__(self):
        self.root = tk.Tk()

        # 1. Setup Window Geometry and Position (400x400 on the left side)
        # Positioned at x=10, y=200 (Adjust y to place it higher/lower on the left)
        self.root.geometry("400x400+10+200")
        self.root.overrideredirect(True)  # Removes window borders/title bar
        self.root.wm_attributes("-topmost", True)  # Keeps it always on top

        # 2. Make Background Fully Transparent
        # Uses 'gray12' as the chroma key color
        self.root.config(bg="gray12")
        self.root.wm_attributes("-transparentcolor", "gray12")

        # 3. Create the Text Label
        # Big font size so characters are easily visible
        self.label = tk.Label(
            self.root, text="", font=("Segoe UI", 48), fg="white", bg="gray12"
        )
        self.label.pack(expand=True)

        # 4. Apply Windows Click-Through Styles via Win32 API
        self.make_window_click_through()

        # 5. Start the Random Unicode Loop
        self.update_character()

    def make_window_click_through(self):
        """Forces the window to ignore mouse clicks and pass them to applications behind it."""
        # Get the window handle (HWND) of the tkinter root window
        hwnd = win32gui.GetParent(self.root.winfo_id())

        # Retrieve current extended window styles
        current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        # Add WS_EX_LAYERED and WS_EX_TRANSPARENT flags
        # WS_EX_TRANSPARENT makes the window click-through
        new_style = (
            current_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        )

        # Apply the new styles
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)

    def get_random_unicode_char(self):
        """Generates a random character from common Windows-supported Unicode blocks.

        Avoids control characters and unassigned ranges.
        """
        # Dictionary of safe, highly compatible hex ranges on standard Windows installations
        ranges = [
            (0x2100, 0x214F),  # Letterlike Symbols
            (0x2190, 0x21FF),  # Arrows
            (0x2200, 0x22FF),  # Mathematical Operators
            (0x2300, 0x23FF),  # Miscellaneous Technical
            (0x25A0, 0x25FF),  # Geometric Shapes
            (0x2600, 0x26FF),  # Miscellaneous Symbols (Stars, Weather, Chess)
            (0x2700, 0x27BF),  # Dingbats
        ]

        # Select a random range, then select a random integer inside that range
        chosen_range = random.choice(ranges)
        random_code_point = random.randint(chosen_range[0], chosen_range[1])

        # Convert the integer code point into a character string
        return chr(random_code_point)

    def update_character(self):
        """Updates the text with a new character and schedules the next run dynamically."""
        # Pick and render the random character
        new_char = self.get_random_unicode_char()
        self.label.config(text=new_char)

        # Pick a random delay between 2.500 and 10,000 milliseconds (2,5 to 10 seconds)
        random_delay_ms = random.randint(2500, 10000)

        # Use Tkinter's non-blocking loop to schedule the next update execution
        self.root.after(random_delay_ms, self.update_character)

    def run(self):
        # Start the Tkinter GUI thread
        self.root.mainloop()


if __name__ == "__main__":
    overlay = TransparentOverlay()
    overlay.run()
