import tkinter as tk
from tkinter import ttk
import time

def start_loading():
    max_value = 100
    for i in range(max_value + 1):
        progress['value'] = i
        root.update_idletasks()
        time.sleep(0.05)  # Loading speed
    root.destroy()  # Close window when done

root = tk.Tk()
root.title("Loading...")

# Set window size
window_width = 400
window_height = 100

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position for centering window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)  # Disable resizing

# Set background color and padding
root.configure(bg='black')

# Create progress bar
progress = ttk.Progressbar(root, orient='horizontal', length=350, mode='determinate')
progress.pack(pady=30)

# Label above the progress bar
label = tk.Label(root, text="Loading...", fg="white", bg="black", font=("Arial", 16))
label.pack()

# Start loading after window appears
root.after(100, start_loading)

root.mainloop()
