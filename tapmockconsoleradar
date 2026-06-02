import random
import time

# Mock class representing an enemy unit
class EnemyUnit:
    def __init__(self, name, strength, position):
        self.name = name
        self.strength = strength
        self.position = position  # position could be a tuple (x, y)

    def __str__(self):
        return f"{self.name} (Strength: {self.strength}) at {self.position}"

# Mock class representing the radar
class FantasyWarfareRadar:
    def __init__(self):
        self.enemies = []

    def detect_enemy(self):
        # Generate a mock enemy with random properties
        names = ["Orc", "Goblin", "Troll", "Wraith", "Dragon"]
        name = random.choice(names)
        strength = random.randint(1, 10)
        position = (random.randint(0, 100), random.randint(0, 100))
        enemy = EnemyUnit(name, strength, position)
        self.enemies.append(enemy)
        print(f"Radar Alert: Detected enemy - {enemy}")

    def run(self, duration_seconds=120):
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            interval = random.uniform(0, 30)
            time.sleep(interval)
            self.detect_enemy()

# Run the radar simulation for 2 minutes (120 seconds)
if __name__ == "__main__":
    radar = FantasyWarfareRadar()
    radar.run()
