import tkinter as tk
import random
import hashlib
import math
import numpy as np
import sounddevice as sd

# --- CONFIGURATION ---
GRID_SIZE = 10
CENTER = (GRID_SIZE // 2, GRID_SIZE // 2)

ARCHETYPES = [
    "Recon Drone", "Heavy Cruiser", "Scout Vessel", 
    "Bio-Sign", "Space Debris", "Plasma Cloud", 
    "Stealth Frigate", "Comet Fragment", "Cat", "Terran", "Zerg", "Protoss"
]

HOSTILITY_MODES = {
    "FRIENDLY": {"label": "FRIENDLY", "color": "#00FF66", "symbol": "[+]"},
    "NEUTRAL":  {"label": "NEUTRAL",  "color": "#FFFF33", "symbol": "[=]"},
    "HOSTILE":  {"label": "HOSTILE",  "color": "#FF3333", "symbol": "[!]"}
}

class RadarOverlay:
    def __init__(self, root):
        self.root = root
        self.log_history = []
        
        print("[1/4] Initializing iDEN Nextel-Chirp Tactical Radar...")
        self.root.title("Tactical Radar Overlay")
        
        # --- OS COMPATIBLE TRANSPARENCY ---
        self.root.overrideredirect(True)       
        self.root.attributes("-topmost", True)   
        self.root.attributes("-alpha", 0.90)     
        
        self.bg_color = "#0a0f0d"
        self.grid_bg = "#0d1410"
        
        self.root.configure(bg=self.bg_color)
        
        # --- SCREEN POSITIONING ---
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 280
        window_height = 430  
        x_offset = screen_width - window_width - 30
        y_offset = 50
        
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
        
        # --- WIDGET SETUP ---
        self.title_label = tk.Label(root, text="SYS_RADAR_ACTIVE", fg="#00FF66", bg=self.bg_color, font=("Courier", 10, "bold"))
        self.title_label.pack(pady=3)
        
        self.canvas = tk.Canvas(root, width=200, height=200, bg=self.grid_bg, highlightbackground="#1a2920", highlightthickness=1)
        self.canvas.pack(pady=5)
        
        self.hash_label = tk.Label(root, text="----------", fg="#FFFFFF", bg=self.bg_color, font=("Courier", 20, "bold"))
        self.hash_label.pack(pady=2)
        
        self.log_box = tk.Text(root, width=36, height=6, bg="#070a08", fg="#00EE55", font=("Courier", 8), borderwidth=0, highlightthickness=0)
        self.log_box.pack(pady=5, padx=10)
        
        print("[4/4] System Armed. Entering background monitoring loop...")
        self.root.withdraw() 
        self.update_radar()

    def generate_blip(self):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        raw_dist = math.sqrt((x - CENTER[0])**2 + (y - CENTER[1])**2)
        distance_meters = int(raw_dist * 150)
        
        salt = f"{random.random()}{x}{y}"
        blip_hash = hashlib.sha256(salt.encode()).hexdigest()[:10].upper()
        archetype = random.choice(ARCHETYPES)

	# CJK Unified Ideographs hex range used for Hanja
        start_hex = 0x4E00
        end_hex = 0x9FFF

	# Generate 4 random characters and join them
        random_hanja_string = "".join(chr(random.randint(start_hex, end_hex)) for _ in range(4))

        
        threat_type = random.choice(["FRIENDLY", "NEUTRAL", "HOSTILE"])
        threat_profile = HOSTILITY_MODES[threat_type]
        
        return {
            "x": x, "y": y, 
            "hash": blip_hash, 
            "type": archetype, 
            "distance": distance_meters,
            "threat": threat_profile,
            "hanja" : random_hanja_string
        }

    def play_nextel_chirp(self, blip_hash, threat_label):
        try:
            sample_rate = 44100
            
            # --- NEXTEL PING PREAMBLE (The classic "Bip-Bip") ---
            # Pulse 1
            t_p1 = np.linspace(0, 0.025, int(sample_rate * 0.025), endpoint=False)
            p1 = np.sin(2 * np.pi * 1800 * t_p1)
            # Gap
            gap = np.zeros(int(sample_rate * 0.015))
            # Pulse 2
            t_p2 = np.linspace(0, 0.035, int(sample_rate * 0.035), endpoint=False)
            p2 = np.sin(2 * np.pi * 1820 * t_p2)
            
            preamble = np.concatenate([p1 * 0.6, gap, p2 * 0.7, gap])
            
            # --- MODULATED DATA BURST ---
            t_mid = np.linspace(0, 0.20, int(sample_rate * 0.20), endpoint=False)
            
            # Base variables seeded by hash
            base_freq = 450 + (int(blip_hash[0:2], 16) * 2)    
            mod_freq = 30 + (int(blip_hash[2:4], 16) % 50)     
            mod_index = 20 + (int(blip_hash[4:6], 16) % 30)    
            
            # Threat variations affect the spike modulation signature
            if threat_label == "HOSTILE":
                mod_index *= 3.0  
                modulator = mod_index * np.sign(np.sin(2 * np.pi * mod_freq * t_mid))
            elif threat_label == "NEUTRAL":
                modulator = mod_index * np.sin(2 * np.pi * mod_freq * t_mid)
            else: # Friendly
                modulator = mod_index * 0.4 * np.sin(2 * np.pi * (mod_freq * 0.6) * t_mid)

            payload = np.sin(2 * np.pi * base_freq * t_mid + modulator)
            
            # --- HARSH SQUELCH TAIL ---
            t_post = np.linspace(0, 0.04, int(sample_rate * 0.04), endpoint=False)
            white_noise = np.random.normal(0, 1, len(t_post))
            
            # Assemble whole sound sequence
            full_signal = np.concatenate([preamble, payload * 0.4, white_noise * 0.25])
            full_signal = np.asarray(full_signal, dtype=np.float32).flatten()
            
            # Rapid fade-ins and fade-outs to emphasize the radio "gate" closing click
            fade_in_len = min(40, len(full_signal))
            fade_out_len = min(200, len(full_signal))
            full_signal[:fade_in_len] *= np.linspace(0.0, 1.0, fade_in_len)
            full_signal[-fade_out_len:] *= np.linspace(1.0, 0.0, fade_out_len)
            
            sd.play(full_signal * 0.28, sample_rate)
        except Exception as e:
            print(f"Audio Error: {e}")

    def draw_grid_canvas(self, blip):
        self.canvas.delete("all")
        cell_size = 20
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1 = c * cell_size + cell_size // 2
                y1 = r * cell_size + cell_size // 2
                
                if r == CENTER[1] and c == CENTER[0]:
                    self.canvas.create_text(x1, y1, text="▲", fill="#00FF66", font=("Courier", 10))
                elif blip and blip["x"] == c and blip["y"] == r:
                    threat_color = blip["threat"]["color"]
                    self.canvas.create_oval(x1-6, y1-6, x1+6, y1+6, fill=threat_color, outline="#FFFFFF", width=1)
                    self.canvas.create_oval(x1-12, y1-12, x1+12, y1+12, outline=threat_color, width=1)
                else:
                    self.canvas.create_text(x1, y1, text="·", fill="#1a3a25", font=("Courier", 12))

    def hide_overlay(self):
        self.root.withdraw()

    def update_radar(self):
        self.root.deiconify()
        
        blip = self.generate_blip()
        self.log_history.append(blip)
        
        self.hash_label.config(text=blip['hanja'], fg=blip["threat"]["color"])
        
        self.draw_grid_canvas(blip)
        self.play_nextel_chirp(blip["hash"], blip["threat"]["label"])
        
        self.log_box.config(state=tk.NORMAL)
        self.log_box.delete('1.0', tk.END)
        for log in self.log_history[-5:]:
            sym = log["threat"]["symbol"]
            log_line = f"{sym} [{log['hash']}] {log['type'][:10]:<10} {log['distance']:>4}m\n"
            self.log_box.insert(tk.END, log_line)
        self.log_box.config(state=tk.DISABLED)
        self.log_box.see(tk.END)
        
        self.root.after(10000, self.hide_overlay)
        
        next_delay_ms = int(random.uniform(0.0, 300.0) * 1000)
        self.root.after(next_delay_ms, self.update_radar)

if __name__ == "__main__":
    root = tk.Tk()
    app = RadarOverlay(root)
    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()
