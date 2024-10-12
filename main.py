import pyxel
import random
from typing import Literal

WIDTH: int = 200
HEIGHT: int = 300
FPS: int = 30

class Pipe:

    """ This class represents the pipe """

    def __init__(self, x: int, y: int, gap: int, width: int = 36, spawn_timer: int = 0) -> None:
        self.x = x
        self.y = y
        self.gap = gap # the size of the opening
        self.width = width # the width of the pipe
        self.spawn_timer = spawn_timer

    def draw_pipe(self):
        # Draw the top pipe's rounded part
        pyxel.blt(self.x, self.y, 0, 0, 44, self.width + 4, 8, 8)  # The rounded top (adjust to your sprite)
        
        # Draw the top pipe's straight section
        pyxel.rect(self.x + 2, 0, self.width, self.y, 11)  # Continues the top part as a rectangle
        
        # Draw the bottom pipe's rounded part
        pyxel.blt(self.x, self.y + self.gap + 8, 0, 0, 28, self.width + 4, 8, 8)  # Rounded cap of bottom pipe

        # Draw the bottom pipe's straight section
        pyxel.rect(self.x + 2, self.y + self.gap + 16, self.width, HEIGHT - (self.y + self.gap + 16), 11)
        
    def get_bounding_boxes(self) -> tuple[tuple[int, Literal[0], int, int], tuple[int, int, int, int]]:

        """ Get the bounding boxes of the top and bottom pipes """

        top_pipe_rect: tuple[int, Literal[0], int, int] = (self.x + 1, 0, self.x + self.width, self.y + 8)
        bottom_pipe_rect: tuple[int, int, int, int] = (self.x + 1 , self.y + self.gap + 8, self.x + self.width, HEIGHT)
        return top_pipe_rect, bottom_pipe_rect
    
class Duck:

    """ This class represents the player (duck) """

    def __init__(self, x: float, y: float, sprite: str, vy: float = 0, dy: float = 0.5, flap_power: float = -3.5) -> None:
        self.x = x
        self.y = y
        self.vy = vy
        self.dy = dy # Gravity
        self.flap_power = flap_power
        self.sprite = sprite
        self.is_flapping = False
    
    def bound(self) -> None:

        """ This is for the top and bottom edge of window"""

        if self.y > HEIGHT - 12:
            self.y = HEIGHT - 12
        elif self.y < 0:
            self.y = 0
    
    def get_bounding_box(self) -> tuple[float, float | int, float | int, float | int]:

        """ Gets the bounding box of the duck """

        return (self.x, self.y, self.x  + 16, self.y + 16)

    def is_colliding(self, pipes: list[Pipe]) -> bool:

        """ Checks for collisions of the duck and the pipes """

        for pipe in pipes:
            top_pipe_rect, bottom_pipe_rect = pipe.get_bounding_boxes()

            # Check pixel-perfect collision with both top and bottom pipe
            if self.is_overlapping_pipe(self.x, self.y, top_pipe_rect) or self.is_overlapping_pipe(self.x, self.y, bottom_pipe_rect):
                return True
        return False

    def is_overlapping_pipe(self, x: float, y: float, pipe_rect: tuple[int, Literal[0] | int, int, int]) -> bool:
        """ Check for pixel-perfect collision between duck sprite and pipe """

        # Loop through every pixel of the duck sprite
        for i in range(16):  # Width of the duck sprite
            for j in range(16):  # Height of the duck sprite
                duck_pixel = pyxel.images[0].pget(int(self.x + i), int(self.y + j))  # Using pyxel.images[0]

                if duck_pixel != pyxel.COLOR_RED:  # COLOR_RED is transparent
                    pipe_x_min, pipe_y_min, pipe_x_max, pipe_y_max = pipe_rect
                    # Check if the current pixel of the duck is within the pipe bounding box
                    if pipe_x_min <= x + i <= pipe_x_max and pipe_y_min <= y + j <= pipe_y_max:
                        pipe_pixel = pyxel.images[0].pget(int(x + i), int(y + j))  # Using pyxel.images[0]
                        # If pipe pixel is not transparent, collision occurred
                        if pipe_pixel != pyxel.COLOR_RED:  
                            return True
        return False

class Game:
    def __init__(self) -> None:
        pyxel.init(WIDTH, HEIGHT, title="Flappy Duck!", fps=FPS)
        self.duck: Duck = Duck(WIDTH // 2, HEIGHT // 2, "duck.pyxres")
        self.pipes: list[Pipe] = [Pipe(WIDTH, random.randint(40, 160), random.randint(60, 90))]
        self.pipe_spawn_timer = 0
        self.score: int = 0
        self.game_over: bool = False
        self.game_start: bool = False
        pyxel.load(self.duck.sprite)
        pyxel.run(self.update, self.draw)
    
    def update_duck(self) -> None:
        self.duck.vy += self.duck.dy
        self.duck.y += self.duck.vy
        
        # If space is pressed, flap (jump)
        if pyxel.btn(pyxel.KEY_SPACE):
            self.duck.vy = self.duck.flap_power
            self.duck.is_flapping = True
        
        if self.duck.vy > 0:
            self.duck.is_flapping = False
        
        self.duck.bound()
    
    def update_pipes(self) -> None:
        for pipe in self.pipes:
            pipe.x -= 2 
        
        self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]
        
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer > 90:  # Every 90 frames (about 3 seconds at 30 FPS)
            new_pipe = Pipe(WIDTH, random.randint(20, 150), random.randint(40, 60))
            self.pipes.append(new_pipe)
            self.pipe_spawn_timer = 0

    def update(self) -> None:

        #while not self.game_start:


        if self.game_over:
            self.game_start = False
            return
        
        self.update_duck()
        self.update_pipes()

        if self.duck.is_colliding(self.pipes):
            print("You lost!")
            self.game_over = True
            
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.rect(0, 0, WIDTH, HEIGHT, 3)
        pyxel.text(20, 20, f"Score: {self.score}", pyxel.COLOR_WHITE, None)
        if self.duck.is_flapping:
            pyxel.blt(self.duck.x, self.duck.y, 0, 0, 0, 16, 16, 8)
        else:
            pyxel.blt(self.duck.x, self.duck.y, 0, 16, 0, 16, 16, 8)
        
        for pipe in self.pipes:
            pipe.draw_pipe()
        
        if self.game_over:
            pyxel.text(20, 30, "Game Over!", pyxel.COLOR_RED, None)

Game()