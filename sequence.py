import tkinter as tk
import win32gui
import win32con
import win32api
import random

class PoE2CrystalOverlay:
    def __init__(self):
        self.root = tk.Tk()
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        
        # Version 2 framework transparency key
        self.trans_color = '#000000'
        self.root.config(bg=self.trans_color)
        self.root.wm_attributes("-transparentcolor", self.trans_color)
        
        self.canvas = tk.Canvas(
            self.root, 
            width=self.screen_width, 
            height=self.screen_height, 
            bg=self.trans_color, 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Initialize pools for text modulation
        self.init_character_pools()
        
        self.make_window_click_through()
        self.draw_ui_shell()
        
        # Start the partial text modulation loop
        self.update_sequence_mask()
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def init_character_pools(self):
        """Builds the collection of characters and sets up the baseline list."""
        # 50 core Hanja characters
        hanja = list("一二三四五六七八九十大小上下左右前後天地日月水火木金土人父母兄弟男女天地人王主玉石田力目口耳手足心身生化")
        # Cyrillic letters
        cyrillic = [chr(i) for i in range(0x0410, 0x044F)] 
        # Latin letters
        latin = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
        # Numeric characters
        numbers = list("0123456789")
        # Arabic letters
        arabic = [chr(i) for i in range(0x0621, 0x064A)]
        
        self.all_chars = hanja + cyrillic + latin + numbers + arabic
        self.mask_length = 36
        
        # Generate the initial starting string so we can mutate it partially later
        self.current_sequence = [random.choice(self.all_chars) for _ in range(self.mask_length)]

    def make_window_click_through(self):
        hwnd = self.root.winfo_id()
        old_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_style = old_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    def draw_crystal_pillar(self, base_x, base_y, width, height, is_right_side=False):
        c_dark = "#15151a"
        c_mid = "#22222e"
        c_light = "#3a3a4f"
        c_edge = "#555570"
        
        offset = -20 if is_right_side else 20
        
        p1 = [
            base_x, base_y,                                
            base_x + width, base_y,                        
            base_x + width + offset, base_y - height + 40, 
            base_x + (width // 2) + offset, base_y - height,
            base_x + offset, base_y - height + 30          
        ]
        self.canvas.create_polygon(p1, fill=c_mid, outline=c_edge, width=2)
        
        facet1 = [
            base_x + (width // 2) + offset, base_y - height,
            base_x + width + offset, base_y - height + 40,
            base_x + (width // 2), base_y
        ]
        self.canvas.create_polygon(facet1, fill=c_light, outline=c_edge, width=1)

        side_offset = -40 if is_right_side else 40
        p2 = [
            base_x + side_offset, base_y,
            base_x + width // 2 + side_offset, base_y,
            base_x + width // 2 + side_offset + (offset // 2), base_y - (height // 1.5),
            base_x + side_offset + (offset // 2), base_y - (height // 1.5) + 20
        ]
        self.canvas.create_polygon(p2, fill=c_dark, outline=c_edge, width=1)

    def draw_ui_shell(self):
        h = self.screen_height
        w = self.screen_width
        
        # --- TOP DISPLAY BANNER ---
        self.canvas.create_rectangle(
            w * 0.32, 0, w * 0.68, 35, 
            fill="#111116", outline="#a2843e", width=2
        )
        
        # Placeholder text object for the sequence
        self.mask_text_id = self.canvas.create_text(
            w * 0.5, 17, 
            text="", 
            fill="#d2b46a", font=("Courier New", 11, "bold")
        )
        
        # --- FIXED VERTICAL BASELINE ---
        crystal_base_y = h - 15
        
        # --- LEFT CRYSTAL ZONE (Hugging left edge) ---
        self.draw_crystal_pillar(base_x=5, base_y=crystal_base_y, width=100, height=350, is_right_side=False)
        
        # --- RIGHT CRYSTAL ZONE (Hugging right edge) ---
        self.draw_crystal_pillar(base_x=w - 125, base_y=crystal_base_y, width=100, height=350, is_right_side=True)

    def update_sequence_mask(self):
        """Mutates only 0 to 4 characters in-place while retaining the rest."""
        # Determine how many character slots to modify this tick (0 to 4 inclusive)
        num_changes = random.randint(0, 4)
        
        if num_changes > 0:
            # Pick unique random slot indices across the sequence length
            indices_to_mutate = random.sample(range(self.mask_length), num_changes)
            for idx in indices_to_mutate:
                self.current_sequence[idx] = random.choice(self.all_chars)
        
        # Convert list back to a displayable text string
        current_text_string = "".join(self.current_sequence)
        
        # Apply the partial text update to the canvas object
        self.canvas.itemconfig(self.mask_text_id, text=current_text_string)
        
        # Maintain your specific speed tracker delay (350 milliseconds)
        self.root.after(350, self.update_sequence_mask)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    overlay = PoE2CrystalOverlay()
    overlay.run()
