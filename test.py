import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button and Score Display")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 40)

# Score
score = 0

# Button
button_color = BLUE
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)  # Centered button

# Function to draw text
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect)
    draw_text(screen, "Click Me", font, WHITE, button_rect.centerx, button_rect.centery)

    # Draw score
    draw_text(screen, f"Score: {score}", font, BLACK, WIDTH // 2, 50)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):  # Check if button clicked
                score += 1  # Increment score

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
