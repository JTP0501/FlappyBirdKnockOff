import pyxel
import random

WIDTH: int = 200
HEIGHT: int = 300
FPS: int = 30

class Pipe:

    """ This class represents the pipe """

    def __init__(self, x: int, y: int, gap: int, width: int = 40, spawn_timer: int = 0) -> None:
        self.x = x
        self.y = y
        self.gap = gap # the size of the opening
        self.width = width # the width of the pipe
        self.pipe: tuple[int, int] = (self.x, self.y) # Obstacle position (x, y)
        self.spawn_timer = spawn_timer

    def draw_pipe(self):
        pyxel.rect(self.x, 0, self.width, self.y, 11) # top pipe
        pyxel.rect(self.x, self.y + self.gap, self.width, HEIGHT - (self.y + self.gap), 11) # bottom pipe

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
        if self.y > HEIGHT - 8:
            self.y = HEIGHT - 8
        elif self.y < 0:
            self.y = 0
    
class Game:
    def __init__(self) -> None:
        pyxel.init(WIDTH, HEIGHT, title="Flappy Duck!", fps=FPS)
        self.duck: Duck = Duck(WIDTH // 2, HEIGHT // 2, "duck.pyxres")
        self.pipes: list[Pipe] = [Pipe(WIDTH, random.randint(50, 150), random.randint(80, 120))]
        self.pipe_spawn_timer = 0
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
            new_pipe = Pipe(WIDTH, random.randint(50, 150), random.randint(40, 60))
            self.pipes.append(new_pipe)
            self.pipe_spawn_timer = 0

    def update(self) -> None:
        self.update_duck()
        self.update_pipes()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.rect(0, 0, WIDTH, HEIGHT, 3)
        if self.duck.is_flapping:
            pyxel.blt(self.duck.x, self.duck.y, 0, 0, 0, 16, 16, 8)
        else:
            pyxel.blt(self.duck.x, self.duck.y, 0, 16, 0, 16, 16, 8)
        
        for pipe in self.pipes:
            pipe.draw_pipe()
Game()