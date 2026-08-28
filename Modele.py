import math
import random

WORLD_SIZE = 4000

class Clock:
    def __init__(self):
        self.tick = 0

    def step(self):
        self.tick += 1

    @property
    def day(self):
        return self.tick // 4

class Climate:
    def __init__(self, rng: random.Random):
        self.rng = rng

    def get_state(self, tick: int):
        slow_season = math.sin(tick * 2 * math.pi / 70.0) * 8.0
        noise = math.sin(tick * 0.45 + self.rng.random())
        opacity = max(0.0, min(1.0, (noise - 0.2) / 0.8)) if noise > 0.2 else 0.12
        eclipse = 1.0 if (tick % 4 == 0) else 0.0
        insolation = max(0.0, (1.0 - opacity) * (1.0 - (eclipse * 0.3)))
        temp = -18.0 + slow_season + (insolation * 14.0)
        
        return {
            "insolation": insolation,
            "opacity": opacity,
            "temperature": temp
        }

class Vein:
    def __init__(self, points, width=3):
        self.points = points
        self.width = width

    def update(self, tick: int, rng: random.Random):
        if tick > 0 and tick % 28 == 0:
            new_pts = []
            for x, y in self.points:
                dx = rng.choice([-15, 0, 15])
                dy = rng.choice([-15, 0, 15])
                new_pts.append((max(0, min(WORLD_SIZE, x + dx)), max(0, min(WORLD_SIZE, y + dy))))
            self.points = new_pts

class Column:
    def __init__(self, x, y, radius, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.height = height

class SimulationModel:
    def __init__(self, seed: int = 1742):
        self.seed = seed
        self.rng = random.Random(seed)
        self.clock = Clock()
        self.climate = Climate(self.rng)
        
        # Veine thermique qui traverse l'île
        self.veins = [
            Vein([(200, 2600), (1200, 2300), (2000, 2000), (2800, 1800), (3800, 1400)], width=3)
        ]
        
        # Île ocre principale et blocs de terrain (coordonnées monde)
        self.ocre_zone = (1200, 1000, 2800, 2600)
        
        # Colonnes de Prototaxites décoratives/simulées (x, y, rayon, hauteur)
        self.columns = []
        for _ in range(25):
            cx = self.rng.randint(1400, 2600)
            cy = self.rng.randint(1200, 2400)
            r = self.rng.randint(12, 28)
            h = self.rng.randint(80, 220)
            self.columns.append(Column(cx, cy, r, h))
        # Trier par Y pour l'affichage en perspective isometric/profondeur
        self.columns.sort(key=lambda c: c.y)

        # Arthropodes & Amphibiens
        self.arthropods = [(self.rng.randint(1600, 2400), self.rng.randint(1400, 2200)) for _ in range(24)]
        self.amphibians = [(self.rng.randint(2200, 2500), self.rng.randint(2000, 2300)) for _ in range(6)]
        
        self.current_climate = self.climate.get_state(0)

    def update(self):
        self.clock.step()
        tick = self.clock.tick
        self.current_climate = self.climate.get_state(tick)
        for vein in self.veins:
            vein.update(tick, self.rng)
            
        # Animation des arthropodes le long des chemins
        new_arthro = []
        for x, y in self.arthropods:
            nx = x + self.rng.randint(-4, 6)
            ny = y + self.rng.randint(-3, 3)
            new_arthro.append((nx, ny))
        self.arthropods = new_arthro