# Name: Noah Dumas
# Course: CS 3080
# Project: Simple Snake Game with Pygame

# ==============================
# Imports
# ==============================
import pygame
import random

# ==============================
# Grid configuration
# ==============================
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# ==============================
# Color configuration (GUI)
# ==============================
COLOR_BACKGROUND = (0, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_FOOD = (255, 0, 0)
COLOR_TEXT = (255, 255, 255)


class SnakeGame:
    # ==============================
    # Initialization and game setup
    # ==============================
    def __init__(self):
        # Initialize pygame, window, clock, and font
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)

        # Set initial game state
        self.reset_game()

    # ==============================
    # Game state reset
    # ==============================
    def reset_game(self):
        # Place the starting snake in the middle of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Snake is stored as a list of (x, y) grid positions
        self.snake = [(start_x, start_y)]

        # No movement until the player presses a movement key
        self.direction = (0, 0)  # (dx, dy)
        self.started = False

        # Score is number of food pieces eaten
        self.score = 0

        # Game over flag
        self.game_over = False

        # Place the first food item
        self.spawn_food()

    # ==============================
    # Food placement logic
    # ==============================
    def spawn_food(self):
        # Place food at a random grid cell that is not part of the snake
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1)
            food_y = random.randint(0, GRID_HEIGHT - 1)
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    # ==============================
    # Controls and input handling
    # ==============================
    def handle_input(self):
        # Handle all pygame events for this frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Window close button
                return False

            if event.type == pygame.KEYDOWN:
                # ESC key quits the game
                if event.key == pygame.K_ESCAPE:
                    return False

                # Movement keys while the game is running
                if not self.game_over:
                    # W key moves up
                    if event.key == pygame.K_w:
                        # Prevent direct reversal of direction
                        if self.direction != (0, 1):
                            self.direction = (0, -1)
                            self.started = True
                    # S key moves down
                    elif event.key == pygame.K_s:
                        if self.direction != (0, -1):
                            self.direction = (0, 1)
                            self.started = True
                    # A key moves left
                    elif event.key == pygame.K_a:
                        if self.direction != (1, 0):
                            self.direction = (-1, 0)
                            self.started = True
                    # D key moves right
                    elif event.key == pygame.K_d:
                        if self.direction != (-1, 0):
                            self.direction = (1, 0)
                            self.started = True

                # SPACE restarts the game after game over
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset_game()

        return True

    # ==============================
    # Game update logic (snake movement, collisions)
    # ==============================
    def update_snake(self):
        # Skip updates if game is over
        if self.game_over:
            return

        # Snake does not move until the player starts the game
        if not self.started:
            return

        # Compute next head position using current direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head_x = head_x + dx
        new_head_y = head_y + dy
        new_head = (new_head_x, new_head_y)

        # Check collision with walls
        if (
            new_head_x < 0
            or new_head_x >= GRID_WIDTH
            or new_head_y < 0
            or new_head_y >= GRID_HEIGHT
        ):
            self.game_over = True
            return

        # Check collision with the snake body
        if new_head in self.snake:
            self.game_over = True
            return

        # Insert new head at the beginning of the list
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
            # Tail is not removed so the snake grows
        else:
            # Remove last segment to move without growing
            self.snake.pop()

    # ==============================
    # Rendering helpers (GUI)
    # ==============================
    def draw_grid_cell(self, position, color):
        # Draw a single grid cell as a filled rectangle
        x, y = position
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE
        rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    # ==============================
    # Rendering main frame (GUI)
    # ==============================
    def draw(self):
        # Clear the screen
        self.screen.fill(COLOR_BACKGROUND)

        # Draw food
        self.draw_grid_cell(self.food, COLOR_FOOD)

        # Draw snake segments
        for segment in self.snake:
            self.draw_grid_cell(segment, COLOR_SNAKE)

        # Draw score text
        score_text = f"Score: {self.score}"
        score_surface = self.font.render(score_text, True, COLOR_TEXT)
        self.screen.blit(score_surface, (10, 10))

        # Draw game over message
        if self.game_over:
            message = "Game Over."
            message_surface = self.font.render(message, True, COLOR_TEXT)
            message_rect = message_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            self.screen.blit(message_surface, message_rect)

        # Update the display
        pygame.display.flip()

    # ==============================
    # Main game loop
    # ==============================
    def run(self):
        running = True
        fps = 10  # Frames per second

        while running:
            # Process events (controls)
            running = self.handle_input()

            # Update game state (logic)
            self.update_snake()

            # Draw everything (GUI)
            self.draw()

            # Control the frame rate
            self.clock.tick(fps)

        # Clean up pygame when the loop ends
        pygame.quit()


# ==============================
# Program entry point
# ==============================
def main():
    # Create a SnakeGame object and start the main loop
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
