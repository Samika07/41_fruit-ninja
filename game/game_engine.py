import pygame
import random
from .fruit import Fruit


# Game Engine

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOMB_BLACK = (30, 30, 30)

FRUIT_COLORS = [
    (220, 60, 60),
    (230, 140, 40),
    (230, 200, 40),
    (90, 180, 90)
]


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Game objects
        self.fruits = []
        self.trail = []

        # Default difficulty values
        self.spawn_interval = 55
        self._spawn_timer = 0
        self.bomb_chance = 0.15
        self.speed_scale = 1.0

        # Game state
        self.lives = 3
        self.score = 0
        self.game_over = False

        # Fonts
        self.font = pygame.font.SysFont(
            "Arial",
            28
        )

        self.game_over_font = pygame.font.SysFont(
            "Arial",
            56,
            bold=True
        )

        self.final_score_font = pygame.font.SysFont(
            "Arial",
            36
        )

        self.instruction_font = pygame.font.SysFont(
            "Arial",
            24
        )

        # ------------------------------------------------
        # Sound effects
        # ------------------------------------------------

        self.slice_sound = None
        self.bomb_sound = None
        self.game_over_sound = None

        try:
            self.slice_sound = pygame.mixer.Sound(
                "sounds/slice.wav"
            )

            self.bomb_sound = pygame.mixer.Sound(
                "sounds/bomb.wav"
            )

            self.game_over_sound = pygame.mixer.Sound(
                "sounds/game_over.wav"
            )

            self.slice_sound.set_volume(0.5)
            self.bomb_sound.set_volume(0.7)
            self.game_over_sound.set_volume(0.7)

        except pygame.error as error:
            print(
                "Warning: Could not load sound effects:",
                error
            )

    # ----------------------------------------------------
    # Spawn fruit / bomb
    # ----------------------------------------------------

    def spawn_fruit(self):

        x = random.randint(
            60,
            self.width - 60
        )

        vy = (
            -random.uniform(13, 16)
            * self.speed_scale
        )

        vx = random.uniform(
            -2,
            2
        )

        gravity = 0.35

        kind = (
            "bomb"
            if random.random() < self.bomb_chance
            else "fruit"
        )

        fruit = Fruit(
            x,
            self.height + 30,
            vx,
            vy,
            gravity,
            kind=kind
        )

        fruit.color = (
            BOMB_BLACK
            if kind == "bomb"
            else random.choice(FRUIT_COLORS)
        )

        self.fruits.append(fruit)

    # ----------------------------------------------------
    # Event handling
    # ----------------------------------------------------

    def handle_event(self, event):

        # Ignore gameplay input after Game Over
        if self.game_over:
            return

        if event.type == pygame.MOUSEMOTION:
            self._handle_motion(event.pos)

    # ----------------------------------------------------
    # Mouse swipe detection
    # ----------------------------------------------------

    def _handle_motion(self, pos):

        # No previous mouse position yet
        if not self.trail:
            self.trail.append(pos)
            return

        previous_pos = self.trail[-1]

        # Check the complete mouse movement segment
        # instead of checking only the current mouse point.
        for fruit in self.fruits:

            if (
                not fruit.sliced
                and fruit.intersects_segment(
                    previous_pos,
                    pos
                )
            ):
                self._slice(fruit)

        # Add current mouse position to trail
        self.trail.append(pos)

        # Keep trail at a reasonable size
        if len(self.trail) > 15:
            self.trail.pop(0)

    # ----------------------------------------------------
    # Slice fruit / bomb
    # ----------------------------------------------------

    def _slice(self, fruit):

        fruit.sliced = True

        if fruit.kind == "bomb":

            # Bomb sound
            if self.bomb_sound is not None:
                self.bomb_sound.play()

            self._trigger_game_over()

        else:

            # Fruit slicing sound
            if self.slice_sound is not None:
                self.slice_sound.play()

            self.score += 1

    # ----------------------------------------------------
    # Game Over
    # ----------------------------------------------------

    def _trigger_game_over(self):

        # Prevent Game Over from being triggered repeatedly
        if self.game_over:
            return

        self.game_over = True

        # Game Over sound
        if self.game_over_sound is not None:
            self.game_over_sound.play()

    # ----------------------------------------------------
    # Input
    # ----------------------------------------------------

    def handle_input(self):
        # The game is mouse driven.
        pass

    # ----------------------------------------------------
    # Update game state
    # ----------------------------------------------------

    def update(self):

        # Stop gameplay updates after Game Over
        if self.game_over:
            return

        # Spawn timer
        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:

            self._spawn_timer = 0

            self.spawn_fruit()

        # Update all fruits
        still_alive = []

        for fruit in self.fruits:

            fruit.update()

            # Remove sliced fruit
            if fruit.sliced:
                continue

            # Check if fruit has left the screen
            if fruit.off_screen(self.height):

                # Missing a normal fruit costs a life
                if fruit.kind == "fruit":
                    self.lives -= 1

                continue

            still_alive.append(fruit)

        self.fruits = still_alive

        # Game Over if all lives are lost
        if self.lives <= 0:
            self._trigger_game_over()

    # ----------------------------------------------------
    # Rendering
    # ----------------------------------------------------

    def render(self, screen):

        # Normal gameplay screen
        if not self.game_over:

            # Draw fruits and bombs
            for fruit in self.fruits:

                color = getattr(
                    fruit,
                    "color",
                    WHITE
                )

                pygame.draw.circle(
                    screen,
                    color,
                    (
                        int(fruit.x),
                        int(fruit.y)
                    ),
                    fruit.radius
                )

            # Draw blade trail
            if len(self.trail) >= 2:

                pygame.draw.lines(
                    screen,
                    WHITE,
                    False,
                    self.trail,
                    3
                )

            # Score
            score_text = self.font.render(
                f"Score: {self.score}",
                True,
                WHITE
            )

            screen.blit(
                score_text,
                (10, 10)
            )

            # Lives
            lives_text = self.font.render(
                f"Lives: {self.lives}",
                True,
                WHITE
            )

            screen.blit(
                lives_text,
                (
                    self.width - 130,
                    10
                )
            )

        # Game Over screen
        else:
            self._render_game_over(screen)

    # ----------------------------------------------------
    # Game Over screen
    # ----------------------------------------------------

    def _render_game_over(self, screen):

        # Dark overlay
        overlay = pygame.Surface(
            (
                self.width,
                self.height
            )
        )

        overlay.fill(BLACK)
        overlay.set_alpha(220)

        screen.blit(
            overlay,
            (0, 0)
        )

        # GAME OVER text
        game_over_text = self.game_over_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        game_over_rect = game_over_text.get_rect(
            center=(
                self.width // 2,
                self.height // 2 - 100
            )
        )

        screen.blit(
            game_over_text,
            game_over_rect
        )

        # Final score
        score_text = self.final_score_font.render(
            f"Final Score: {self.score}",
            True,
            WHITE
        )

        score_rect = score_text.get_rect(
            center=(
                self.width // 2,
                self.height // 2
            )
        )

        screen.blit(
            score_text,
            score_rect
        )

        # Continue instruction
        instruction_text = self.instruction_font.render(
            "Press any key to continue",
            True,
            WHITE
        )

        instruction_rect = instruction_text.get_rect(
            center=(
                self.width // 2,
                self.height // 2 + 70
            )
        )

        screen.blit(
            instruction_text,
            instruction_rect
        )