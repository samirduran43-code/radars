import tkinter as tk
import time
from screeninfo import get_monitors

class PredatorGauntletClock:
    def __init__(self):
        self.root = tk.Tk()
        
        # 1. Target the secondary display cleanly
        self.setup_multi_monitor()
        
        # 2. Make window borderless and float on top
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # 3. Apply True Chroma-Key Transparency
        transparent_color = '#000001'
        self.root.config(bg=transparent_color)
        self.root.wm_attributes("-transparentcolor", transparent_color)
        
        try:
            self.root.wm_attributes("-transparent", True)
        except tk.TclError:
            pass

        # 4. Create vector canvas
        self.canvas = tk.Canvas(self.root, bg=transparent_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Authentic Sci-Fi Predator Gauntlet Color Scheme
        self.color_on = "#FF0000"   # Vicious glowing cinematic Blood Red
        self.color_off = "#260000"  # Clearly visible unlit display trace
        
        # Map 0-9 to 11-Segment Yautja Gauntlet Array Map
        # Segments index representation:
        # [0: Top-Left, 1: Top-Right, 2: Mid-Top-Left-Diag, 3: Mid-Top-Right-Diag, 
        #  4: Center-Top-Vert, 5: Center-Bottom-Vert, 6: Mid-Bottom-Left-Diag, 
        #  7: Mid-Bottom-Right-Diag, 8: Bottom-Left, 9: Bottom-Right, 10: Horizontal-Spur]
        self.segment_map = {
            '0': (1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0),
            '1': (1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0),
            '2': (1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0),
            '3': (0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
            '4': (1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0),
            '5': (0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1),
            '6': (0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0),
            '7': (1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0),
            '8': (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
            '9': (1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1),
            ' ': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        }

        # Bind Escape key to quit
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Loop execution
        self.root.after(10, self.draw_clock)
        self.root.mainloop()

    def setup_multi_monitor(self):
        """Finds secondary monitor dimensions and offsets dynamically."""
        monitors = get_monitors()
        if len(monitors) > 1:
            target_monitor = monitors[1]
        else:
            target_monitor = monitors[0]
            print("Secondary monitor not found. Running on primary display.")

        geom_string = f"{target_monitor.width}x{target_monitor.height}+{target_monitor.x}+{target_monitor.y}"
        self.root.geometry(geom_string)
        self.width = target_monitor.width
        self.height = target_monitor.height

    def draw_yautja_digit(self, x_offset, y_offset, size, digit):
        """Draws the screen-accurate complex 11-segment Predator terminal characters."""
        w = size
        h = size * 1.8
        t = size * 0.08  # Capsule width
        
        states = self.segment_map.get(digit, self.segment_map[' '])
        
        # Coordinates defining the geometric 11-segment mask
        segments = [
            # 0: Outer Top-Left Tick
            [0, 0, t, 0, t, h*0.3, 0, h*0.3],
            # 1: Outer Top-Right Tick
            [w-t, 0, w, 0, w, h*0.3, w-t, h*0.3],
            # 2: Diagonal Inner Top-Left Line
            [t*1.5, t*1.5, t*2.5, t, w/2, h/2-t, w/2-t, h/2-t],
            # 3: Diagonal Inner Top-Right Line
            [w-t*1.5, t*1.5, w-t*2.5, t, w/2, h/2-t, w/2+t, h/2-t],
            # 4: Central Vertical Core Top
            [w/2-t/2, 0, w/2+t/2, 0, w/2+t/2, h/2-t, w/2-t/2, h/2-t],
            # 5: Central Vertical Core Bottom
            [w/2-t/2, h/2+t, w/2+t/2, h/2+t, w/2+t/2, h, w/2-t/2, h],
            # 6: Diagonal Inner Bottom-Left Line
            [w/2-t, h/2+t, w/2, h/2+t, t*2.5, h-t, t*1.5, h-t*1.5],
            # 7: Diagonal Inner Bottom-Right Line
            [w/2+t, h/2+t, w/2, h/2+t, w-t*2.5, h-t, w-t*1.5, h-t*1.5],
            # 8: Outer Bottom-Left Tick
            [0, h*0.7, t, h*0.7, t, h, 0, h],
            # 9: Outer Bottom-Right Tick
            [w-t, h*0.7, w, h*0.7, w, h, w-t, h],
            # 10: Horizontal Spur Left Accent
            [0, h/2-t/2, t*2, h/2-t/2, t*2, h/2+t/2, 0, h/2+t/2]
        ]
        
        # Pass 1: Render unlit trace background grid structure
        for i, coords in enumerate(segments):
            shifted = []
            for j in range(0, len(coords), 2):
                shifted.append(coords[j] + x_offset)
                shifted.append(coords[j+1] + y_offset)
            self.canvas.create_polygon(shifted, fill=self.color_off, outline='#000000', width=1)
            
        # Pass 2: Overlay live glowing active elements
        for i, coords in enumerate(segments):
            if states[i] == 1:
                shifted = []
                for j in range(0, len(coords), 2):
                    shifted.append(coords[j] + x_offset)
                    shifted.append(coords[j+1] + y_offset)
                self.canvas.create_polygon(shifted, fill=self.color_on, outline='#000000', width=1)

    def draw_clock(self):
        """Clears canvas and computes fresh layout mapping based on system clock values."""
        self.canvas.delete("all")
        
        current_time = time.strftime("%H:%M:%S")
        
        digit_size = self.width // 13
        spacing = digit_size * 1.35
        
        total_clock_width = (6 * spacing) + (2 * (digit_size * 0.4))
        start_x = (self.width - total_clock_width) // 2
        start_y = (self.height - (digit_size * 1.8)) // 2
        
        current_x = start_x
        
        for char in current_time:
            if char == ':':
                # Cinematic custom vertical alien separation nodes
                dot_radius = digit_size * 0.08
                dot_x = current_x + (digit_size * 0.2)
                
                self.canvas.create_oval(dot_x, start_y + (digit_size*0.4), dot_x + 2*dot_radius, start_y + (digit_size*0.4) + 2*dot_radius, fill=self.color_on, outline="")
                self.canvas.create_oval(dot_x, start_y + (digit_size*1.4), dot_x + 2*dot_radius, start_y + (digit_size*1.4) + 2*dot_radius, fill=self.color_on, outline="")
                current_x += digit_size * 0.6
            else:
                self.draw_yautja_digit(current_x, start_y, digit_size, char)
                current_x += spacing
                
        self.root.after(250, self.draw_clock)

if __name__ == "__main__":
    PredatorGauntletClock()
