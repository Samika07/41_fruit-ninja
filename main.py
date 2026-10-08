import pygame
from game.game_engine import GameEngine


# --------------------------------------------------------
# Initialize pygame
# --------------------------------------------------------

pygame.init()
pygame.mixer.init()


# --------------------------------------------------------
# Screen
# --------------------------------------------------------

WIDTH = 700
HEIGHT = 600

SCREEN = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Fruit Slice - Pygame Version"
)


# --------------------------------------------------------
# Colors
# --------------------------------------------------------

DARK_BLUE = (20, 25, 45)
WHITE = (255, 255, 255)


# --------------------------------------------------------
# Clock
# --------------------------------------------------------

clock = pygame.time.Clock()

FPS = 60


# --------------------------------------------------------
# Difficulty Menu
# --------------------------------------------------------

def show_difficulty_menu():

    title_font = pygame.font.SysFont(
        "Arial",
        48,
        bold=True
    )

    option_font = pygame.font.SysFont(
        "Arial",
        30
    )

    instruction_font = pygame.font.SysFont(
        "Arial",
        22
    )

    while True:

        SCREEN.fill(DARK_BLUE)

        # Title
        title = title_font.render(
            "SELECT DIFFICULTY",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                WIDTH // 2,
                130
            )
        )

        SCREEN.blit(
            title,
            title_rect
        )

        # Easy
        easy = option_font.render(
            "1 - EASY",
            True,
            WHITE
        )

        SCREEN.blit(
            easy,
            easy.get_rect(
                center=(
                    WIDTH // 2,
                    230
                )
            )
        )

        # Medium
        medium = option_font.render(
            "2 - MEDIUM",
            True,
            WHITE
        )

        SCREEN.blit(
            medium,
            medium.get_rect(
                center=(
                    WIDTH // 2,
                    290
                )
            )
        )

        # Hard
        hard = option_font.render(
            "3 - HARD",
            True,
            WHITE
        )

        SCREEN.blit(
            hard,
            hard.get_rect(
                center=(
                    WIDTH // 2,
                    350
                )
            )
        )

        # Exit
        exit_option = option_font.render(
            "4 - EXIT",
            True,
            WHITE
        )

        SCREEN.blit(
            exit_option,
            exit_option.get_rect(
                center=(
                    WIDTH // 2,
                    410
                )
            )
        )

        # Instructions
        instruction = instruction_font.render(
            "Press a number key to choose",
            True,
            WHITE
        )

        SCREEN.blit(
            instruction,
            instruction.get_rect(
                center=(
                    WIDTH // 2,
                    490
                )
            )
        )

        pygame.display.flip()

        # Handle menu input
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    return "easy"

                elif event.key == pygame.K_2:
                    return "medium"

                elif event.key == pygame.K_3:
                    return "hard"

                elif event.key == pygame.K_4:
                    return None

        clock.tick(FPS)


# --------------------------------------------------------
# Create game engine based on difficulty
# --------------------------------------------------------

def create_engine(difficulty):

    engine = GameEngine(
        WIDTH,
        HEIGHT
    )

    if difficulty == "easy":

        engine.spawn_interval = 70
        engine.bomb_chance = 0.10
        engine.speed_scale = 0.90

    elif difficulty == "medium":

        engine.spawn_interval = 55
        engine.bomb_chance = 0.15
        engine.speed_scale = 1.0

    elif difficulty == "hard":

        engine.spawn_interval = 40
        engine.bomb_chance = 0.25
        engine.speed_scale = 1.10

    return engine


# --------------------------------------------------------
# Play one game
# --------------------------------------------------------

def play_game(engine):

    while True:

        SCREEN.fill(DARK_BLUE)

        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                return False

            # Game Over input
            if engine.game_over:

                if event.type in (
                    pygame.KEYDOWN,
                    pygame.MOUSEBUTTONDOWN
                ):
                    return True

            else:

                engine.handle_event(event)

        # Normal game processing
        engine.handle_input()

        engine.update()

        engine.render(SCREEN)

        pygame.display.flip()

        clock.tick(FPS)


# --------------------------------------------------------
# Main program
# --------------------------------------------------------

def main():

    running = True

    while running:

        # ----------------------------------------------
        # Choose difficulty
        # ----------------------------------------------

        difficulty = show_difficulty_menu()

        # Exit selected
        if difficulty is None:
            break

        # ----------------------------------------------
        # Create new game
        # ----------------------------------------------

        engine = create_engine(
            difficulty
        )

        # ----------------------------------------------
        # Play
        # ----------------------------------------------

        result = play_game(
            engine
        )

        # Window closed
        if not result:
            break

        # Otherwise:
        # Game Over → return to difficulty menu

    pygame.quit()


# --------------------------------------------------------
# Program entry point
# --------------------------------------------------------

if __name__ == "__main__":
    main()