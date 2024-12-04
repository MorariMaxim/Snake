import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
block_size = 40  # Example block size

# Colors
bg_color = (30, 30, 30)  # Dark background
grid_color = (200, 200, 200)  # Light grid
text_color = (255, 255, 255)  # White text

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid with Score")
font = pygame.font.Font(None, 36)  # Define font

# Board settings
rows, columns = 15, 20  # Example dimensions
score = 0

def draw_grid():
    for row in range(rows):
        pygame.draw.line(screen, grid_color, (0, row * block_size), (screen_width, row * block_size))
    for col in range(columns):
        pygame.draw.line(screen, grid_color, (col * block_size, 0), (col * block_size, screen_height))

def draw_score():
    text_surface = font.render(f"Score: {score}", True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, 20))  # Position at the top-center
    screen.blit(text_surface, text_rect)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen and draw everything
    screen.fill(bg_color)
    draw_score()
    draw_grid()

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
