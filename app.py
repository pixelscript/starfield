import random
import math
import app

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

class Starfield(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.stars = self.create_stars(100)  # Create 100 stars
        self.speed = 0.05  # Speed of star movement

    def create_stars(self, num_stars):
        stars = []
        for _ in range(num_stars):
            star = {
                'x': random.uniform(-1, 1),
                'y': random.uniform(-1, 1),
                'z': random.uniform(0.1, 1)
            }
            stars.append(star)
        return stars

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        
        for star in self.stars:
            star['z'] -= self.speed * delta
            if star['z'] <= 0:
                star['x'] = random.uniform(-1, 1)
                star['y'] = random.uniform(-1, 1)
                star['z'] = 1

    def draw(self, ctx):
        clear_background(ctx)  # Clear the screen
        ctx.save()

        ctx.rgb(0, 0, 0).rectangle(-1, -1, 2, 2).fill()  # Black background

        ctx.rgb(1, 1, 1)  # White color for stars
        for star in self.stars:
            sx = star['x'] / star['z']
            sy = star['y'] / star['z']
            size = 0.01 / star['z']

            ctx.save()
            ctx.translate(sx * 100, sy * 100)  # Scaling up the coordinates for better visibility
            ctx.scale(size * 100, size * 100)  # Adjusting the size of the stars
            ctx.arc(0, 0, 1, 0, 2 * math.pi, True).fill()  # Drawing circles with arc method
            ctx.restore()

        ctx.restore()

__app_export__ = Starfield
