import app
import math
import random

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

class Star:
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size

class Starfield(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.stars = self.create_stars(100)

    def create_stars(self, num_stars):
        stars = []
        for _ in range(num_stars):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, 1)
            speed = random.uniform(1, 1.5)
            size = random.uniform(1, 3)
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            stars.append(Star(x, y, speed, size))
        return stars

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        
        for star in self.stars:
            star.x += star.x * star.speed
            star.y += star.y * star.speed
            
            # If the star moves out of bounds, reset it to the center
            if abs(star.x) > 1 or abs(star.y) > 1:
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, 0.1)
                star.x = math.cos(angle) * distance
                star.y = math.sin(angle) * distance
                star.speed = random.uniform(1, 1.5)
                star.size = random.uniform(1, 3)

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()
        ctx.translate(0, 0)
        ctx.scale(1, 1)
        
        for star in self.stars:
            ctx.rgb(1, 1, 1).begin_path()
            ctx.arc(star.x * 120, star.y * 120, star.size, 0, 2 * math.pi, True).fill()
        
        ctx.restore()

__app_export__ = Starfield
