import tkinter as tk
import math
import random
import time
import string
import ctypes

GWL_EXSTYLE = -20
WS_EX_LAYERED = 131072
WS_EX_TRANSPARENT = 32

class TargetBlip:
    def __init__(self, x, y, name, symbol, serial, b_col, d_col, span):
        self.x = x
        self.y = y
        self.name = name
        self.symbol = symbol
        self.serial = serial
        self.color_bright = b_col
        self.color_dim = d_col
        self.spawn_time = time.time()
        self.lifespan = span

class AdvancedRadarOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Radar Overlay")
        
        scr_w = self.root.winfo_screenwidth()
        scr_h = self.root.winfo_screenheight()
        
        # Dimensions adjusted to account for the new 20pt and 16pt font footprints
        window_width = 550
        window_height = 620
        
        pos_x = scr_w - window_width - 40
        pos_y = scr_h - window_height - 60  
        
        geom_string = str(window_width) + "x" + str(window_height) + "+" + str(pos_x) + "+" + str(pos_y)
        self.root.geometry(geom_string)
        
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg="black")
        self.root.wm_attributes("-transparentcolor", "black")

        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        old_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, old_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

        self.canvas = tk.Canvas(root, width=window_width, height=440, bg="black", highlightthickness=0)
        self.canvas.pack(anchor="e")  

        self.console_frame = tk.Frame(root, bg="black")
        self.console_frame.pack(fill="both", expand=True, anchor="e")
        
        self.labels = []
        self.max_logs = 4

        self.angle = 0
        self.center_x = 275  
        self.center_y = 220
        self.radius = 200    

        self.test = True
        self.hostiles = ["Ancient Dragon", "Shadow Orc", "Wraith"]
        self.neutrals = ["Blood Elf", "Goblin Thief", "Griffon"]
        self.creatures = self.hostiles + self.neutrals
        self.active_blips = {}

        self.draw_static_grid()
        self.update_radar_loop()
        
        if self.test:
            self.spawn_fantasy_target_loop()

    def draw_static_grid(self):
        self.canvas.create_oval(self.center_x - 50, self.center_y - 50, self.center_x + 50, self.center_y + 50, outline="#003300", width=1)
        self.canvas.create_oval(self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y + 100, outline="#003300", width=1)
        self.canvas.create_oval(self.center_x - 150, self.center_y - 150, self.center_x + 150, self.center_y + 150, outline="#003300", width=1)
        self.canvas.create_oval(self.center_x - 200, self.center_y - 200, self.center_x + 200, self.center_y + 200, outline="#003300", width=1)
        
        self.canvas.create_line(self.center_x - self.radius, self.center_y, self.center_x + self.radius, self.center_y, fill="#001100")
        self.canvas.create_line(self.center_x, self.center_y - self.radius, self.center_x, self.center_y + self.radius, fill="#001100")

    def generate_serial(self):
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(10))

    def update_radar_loop(self):
        self.canvas.delete("sweep")
        self.canvas.delete("blip")

        current_time = time.time()
        expired_blips = []

        for b_id, blip in list(self.active_blips.items()):
            elapsed = current_time - blip.spawn_time
            
            if elapsed >= blip.lifespan:
                expired_blips.append(b_id)
                continue

            render_color = getattr(blip, 'color_dim' if (elapsed / blip.lifespan) > 0.75 else 'color_bright')
            
            space_char = chr(32)
            open_bracket = chr(91)
            close_bracket = chr(93)
            marker_text = blip.symbol + space_char + blip.name + space_char + open_bracket + blip.serial + close_bracket
            
            self.canvas.create_oval(blip.x-6, blip.y-6, blip.x+6, blip.y+6, fill=render_color, outline="", tags="blip")
            
            # UPGRADED: Font size increased to 20 per your request
            self.canvas.create_text(blip.x+14, blip.y-4, text=marker_text, fill=render_color, font=("Courier", 20, "bold"), anchor="w", tags="blip")

        for b_id in expired_blips:
            if b_id in self.active_blips:
                del self.active_blips[b_id]

        rad = math.radians(self.angle)
        end_x = self.center_x + self.radius * math.cos(rad)
        end_y = self.center_y + self.radius * math.sin(rad)
        
        self.canvas.create_line(self.center_x, self.center_y, end_x, end_y, fill="#00FF00", width=2, tags="sweep")

        self.angle = (self.angle + 3) % 360
        self.root.after(20, self.update_radar_loop)

    def spawn_fantasy_target_loop(self):
        if not self.test:
            return

        roll_success = random.choice([True, False])
        serial_id = self.generate_serial()
        
        if roll_success:
            identity = random.choice(self.creatures)
            display_name = identity
            if identity in self.hostiles:
                symbol = "A"
                b_col = "#FF0000"
                d_col = "#550000"
            else:
                symbol = "O"
                b_col = "#00FFFF"
                d_col = "#005555"
        else:
            display_name = "B0GEY"
            symbol = "X"
            b_col = "#FFAA00"
            d_col = "#553300"

        distance = random.randint(40, self.radius - 25)
        bearing = random.randint(0, 359)
        lifespan = random.uniform(12.0, 20.0)

        rad = math.radians(bearing)
        bx = self.center_x + distance * math.cos(rad)
        by = self.center_y + distance * math.sin(rad)

        blip_id = random.random()
        self.active_blips[blip_id] = TargetBlip(bx, by, display_name, symbol, serial_id, b_col, d_col, lifespan)

        space_char = chr(32)
        open_bracket = chr(91)
        close_bracket = chr(93)
        log_msg = ">> " + symbol + space_char + display_name + space_char + open_bracket + serial_id + close_bracket + " @ " + str(distance) + "m"
        self.log_message(log_msg, b_col)

        next_interval_ms = random.randint(0, 60000)
        self.root.after(next_interval_ms, self.spawn_fantasy_target_loop)

    def log_message(self, text, color):
        # UPGRADED: Font size set to 16, and contrasting dark solid gray background added
        lbl = tk.Label(
            self.console_frame, 
            text=text, 
            fg=color, 
            bg="#111111", 
            font=("Courier", 16, "bold"), 
            anchor="e",
            padx=8,
            pady=2
        )
        lbl.pack(fill="x", padx=15, pady=3, side="top")
        self.labels.append(lbl)

        if len(self.labels) > self.max_logs:
            self.labels.pop(0).destroy()

if __name__ == "__main__":
    main_window = tk.Tk()
    app = AdvancedRadarOverlay(main_window)
    main_window.bind("<Escape>", lambda e: main_window.destroy())
    main_window.mainloop()
