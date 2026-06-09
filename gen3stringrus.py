import itertools
import os

def generate_cyrillic_combinations():
    # Standard 33-letter Russian Cyrillic alphabet (lowercase)
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    # Target the user's desktop directory dynamically
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = os.path.join(desktop_path, "russian_combinations.txt")
    
    # Open the file and write every combination line by line
    with open(output_file, "w", encoding="utf-8") as file:
        for combo in itertools.product(alphabet, repeat=3):
            file.write("".join(combo) + "\n")

if __name__ == "__main__":
    generate_cyrillic_combinations()
