import tkinter as tk
import time
from screeninfo import get_monitors

class RetroSegmentClock:
    def __init__(self):
        self.root = tk.Tk()
        
        # 1. Target the secondary display cleanly using correct indexing
        self.setup_multi_monitor()
        
        # 2. Make window borderless and stay on top
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

        # 4. Create the vector canvas
        self.canvas = tk.Canvas(self.root, bg=transparent_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Optimized High-Contrast 90s Color Scheme
        self.color_on = "#33FF33"   # Classic bright electronics green
        self.color_off = "#0a290a"  # Deep, understated shadow trace

        # Map 0-9 to 7-segment states
        self.segment_map = {
            '0': (1, 1, 1, 0, 1, 1, 1),
            '1': (0, 0, 1, 0, 0, 1, 0),
            '2': (1, 0, 1, 1, 1, 0, 1),
            '3': (1, 0, 1, 1, 0, 1, 1),
            '4': (0, 1, 1, 1, 0, 1, 0),
            '5': (1, 1, 0, 1, 0, 1, 1),
            '6': (1, 1, 0, 1, 1, 1, 1),
            '7': (1, 0, 1, 0, 0, 1, 0),
            '8': (1, 1, 1, 1, 1, 1, 1),
            '9': (1, 1, 1, 1, 0, 1, 1),
            ' ': (0, 0, 0, 0, 0, 0, 0)
        }

        # Bind 'Escape' key to close the clock easily
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Initial draw trigger
        self.root.after(10, self.draw_clock)
        self.root.mainloop()

    def setup_multi_monitor(self):
        """Fixes the AttributeError by correctly indexing the monitors list."""
        monitors = get_monitors()
        
        # Pull the second element from the list if it exists
        if len(monitors) > 1:
            target_monitor = monitors[1]  # <--- Index 1 is the secondary monitor
        else:
            target_monitor = monitors[0]  # <--- Fallback to primary if single monitor
            print("Secondary monitor not found. Running on primary display.")

        geom_string = f"{target_monitor.width}x{target_monitor.height}+{target_monitor.x}+{target_monitor.y}"
        self.root.geometry(geom_string)
        self.width = target_monitor.width
        self.height = target_monitor.height

    def draw_digit(self, x_offset, y_offset, size, digit):
        """Draws clean, high-readability segmented shapes with structural air gaps."""
        w = size
        h = size * 1.8
        t = size * 0.13  # Segment thickness
        g = size * 0.02  # Gaps between segments
        
        states = self.segment_map.get(digit, self.segment_map[' '])
        
        segments = [
            # 0: Top
            ([t+g, 0, w-t-g, 0, w-2*t-g, t, 2*t+g, t], 0),
            # 1: Top-Left
            ([0, t+g, t, 2*t+g, t, h/2-t/2-g, 0, h/2-g], 1),
            # 2: Top-Right
            ([w-t, 2*t+g, w, t+g, w, h/2-g, w-t, h/2-t/2-g], 2),
            # 3: Middle
            ([2*t+g, h/2-t/2, w-2*t-g, h/2-t/2, w-t-g, h/2+t/2, t+g, h/2+t/2], 3),
            # 4: Bottom-Left
            ([0, h/2+g, t, h/2+t/2+g, t, h-2*t-g, 0, h-t-g], 4),
            # 5: Bottom-Right
            ([w-t, h/2+t/2+g, w, h/2+g, w, h-t-g, w-t, h-2*t-g], 5),
            # 6: Bottom
            ([2*t+g, h-t, w-2*t-g, h-t, w-t-g, h, t+g, h], 6)
        ]
        
        # STEP 1: Draw the background hardware traces
        for coords, index in segments:
            shifted_coords = []
            for i in range(0, len(coords), 2):
                shifted_coords.append(coords[i] + x_offset)
                shifted_coords.append(coords[i+1] + y_offset)
            self.canvas.create_polygon(shifted_coords, fill=self.color_off, outline='#000000', width=1)
            
        # STEP 2: Overlay active illuminated segments
        for coords, index in segments:
            if states[index] == 1:
                shifted_coords = []
                for i in range(0, len(coords), 2):
                    shifted_coords.append(coords[i] + x_offset)
                    shifted_coords.append(coords[i+1] + y_offset)
                self.canvas.create_polygon(shifted_coords, fill=self.color_on, outline='#000000', width=1)

    def draw_clock(self):
        """Clears canvas and updates layout instantly to align with local system clock."""
        self.canvas.delete("all")
        
        current_time = time.strftime("%H:%M:%S")
        
        digit_size = self.width // 12
        spacing = digit_size * 1.3
        
        total_clock_width = (6 * spacing) + (2 * (digit_size * 0.4))
        start_x = (self.width - total_clock_width) // 2
        start_y = (self.height - (digit_size * 1.8)) // 2
        
        current_x = start_x
        
        for char in current_time:
            if char == ':':
                dot_radius = digit_size * 0.08
                dot_x = current_x + (digit_size * 0.2)
                
                self.canvas.create_oval(dot_x, start_y + (digit_size*0.5), dot_x + 2*dot_radius, start_y + (digit_size*0.5) + 2*dot_radius, fill=self.color_on, outline="")
                self.canvas.create_oval(dot_x, start_y + (digit_size*1.3), dot_x + 2*dot_radius, start_y + (digit_size*1.3) + 2*dot_radius, fill=self.color_on, outline="")
                current_x += digit_size * 0.6
            else:
                self.draw_digit(current_x, start_y, digit_size, char)
                current_x += spacing
                
        self.root.after(250, self.draw_clock)

if __name__ == "__main__":
    RetroSegmentClock()
