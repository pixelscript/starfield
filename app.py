import app
import math
import random
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import *
from tildagonos import tildagonos
import asyncio
class Star:
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.speed = speed
        self.size = size

class Starfield(app.App):
    def __init__(self):
        self.max_speed = 1.3
        self.alpha = False
        self.button_states = Buttons(self)
        eventbus.emit(PatternDisable())
        self._make_black()
        self.stars = self.create_stars(100)
        self.colors = [
            (1, 1, 1),  # White
            (0, 1, 0),  # Green
            (1, 0, 0),  # Red
            (0, 0, 1),  # Blue
            (1, 1, 0),  # Yellow
            (0, 1, 1),  # Cyan
            (1, 0, 1),  # Magenta
            (1, 0.5, 0),  # Orange
            (0.5, 0, 0.5),  # Purple
            (0.5, 0.5, 0.5)  # Gray
        ]
        self.colors_neo = [
            (255, 255, 255),  # White
            (0, 255, 0),      # Green
            (255, 0, 0),      # Red
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (0, 255, 255),    # Cyan
            (255, 0, 255),    # Magenta
            (255, 128, 0),    # Orange
            (128, 0, 128),    # Purple
            (128, 128, 128)   # Gray
        ]
        self.current_color_index = 0
        
    def _make_black(self):
        asyncio.sleep(0.5)
        for i in range(1, 13):
            tildagonos.leds[i] = (0, 0, 0)
        tildagonos.leds.write()
    
    def make_random_white(self):
        for i in range(1, 13):
            if random.random() < 0.5:
                tildagonos.leds[i] = (self.colors_neo[self.current_color_index])
            else:
                tildagonos.leds[i] = (0, 0, 0)
        tildagonos.leds.write()

    def create_stars(self, num_stars):
        stars = []
        for _ in range(num_stars):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, 1)
            speed = random.uniform(1, 2)
            size = random.uniform(1, 3)
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            stars.append(Star(x, y, speed, size))
        return stars

    def update(self, delta):
        self.make_random_white()
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        
        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.alpha = not self.alpha
            self.button_states.clear()
        
        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.button_states.clear()

        for star in self.stars:
            # Update previous position before moving the star
            star.prev_x = star.x
            star.prev_y = star.y
            
            star.x += star.x * star.speed
            star.y += star.y * star.speed
            
            # If the star moves out of bounds, reset it to the center
            if abs(star.x) > 1 or abs(star.y) > 1:
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, 0.2)
                star.x = math.cos(angle) * distance
                star.y = math.sin(angle) * distance
                star.prev_x = star.x
                star.prev_y = star.y
                star.speed = random.uniform(1, self.max_speed)
                star.size = random.uniform(1, 3)

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()
        ctx.translate(0, 0)
        ctx.scale(1, 1)
        
        # Get the current color
        current_color = self.colors[self.current_color_index]
        
        # Draw the stars with motion blur and transparency
        for star in self.stars:
            if self.alpha:
                distance_from_center = math.sqrt(star.x**2 + star.y**2)
                alpha = distance_from_center
                ctx.rgba(current_color[0], current_color[1], current_color[2], alpha).begin_path()
            else:
                ctx.rgb(*current_color).begin_path()
            ctx.move_to(star.prev_x * 120, star.prev_y * 120)
            ctx.line_to(star.x * 120, star.y * 120)
            ctx.stroke()
            ctx.arc(star.x * 120, star.y * 120, star.size, 0, 2 * math.pi, True).fill()
        
        ctx.restore()

__app_export__ = Starfield
