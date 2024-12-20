import sys
from Board import *
from GraphicalBoard import *
import pygame

class Game:
    """
    A class to represent the Snake game.
    """
    
    def __init__(self, board_rows, board_columns, board_obstacles, block_size, snake_speed, bg_color, grid_color, snake_color, food_color) -> None:
        """
        Initialize the game with the given parameters.
        
        Args:
            board_rows (int): Number of rows in the board.
            board_columns (int): Number of columns in the board.
            board_obstacles (list): List of obstacles on the board.
            block_size (int): Size of each block in pixels.
            snake_speed (int): Speed of the snake.
            bg_color (tuple): Background color.
            grid_color (tuple): Grid color.
            snake_color (tuple): Snake color.
            food_color (tuple): Food color.
        """
        pygame.init()

        
        self.board_rows = board_rows
        self.board_columns = board_columns
        self.board_obstacles = board_obstacles
        self.snake_speed = snake_speed
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.snake_color = snake_color
        self.food_color = food_color
        
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
                
        self.score = 0
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        self.block_size = block_size
        
        self.best_score = 0
        self.current_score = 0
        
        self.score_height = 50
        self.screen_width = board_columns * self.block_size 
        self.screen_height = self.board_rows * self.block_size + self.score_height
        

        self.init_boards()
        
    def init_boards(self):
        """
        Initialize the game boards by setting up the screen, board, and graphical board.
        """
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        grid_rect = pygame.Rect(0, self.score_height, self.screen_width, self.screen_height - self.score_height)
        self.board_screen = self.screen.subsurface(grid_rect)
        self.score_screen = self.screen.subsurface(pygame.Rect(0, 0, self.screen_width, self.score_height))
        
        self.board = Board(self.board_rows, self.board_columns, self.board_obstacles)
        self.graphical_board = GraphicalBoard(self.board, self.block_size, self.snake_speed, self.bg_color, self.grid_color, self.snake_color, self.food_color, self.board_screen)
        
    def start_game(self):
        """
        Start the game loop by setting the initial direction of the snake and entering the game loop.
        """
        self.board.set_direction((0, 1))
        
        self.game_loop()

    def draw_score(self, current_score, best_score):
        """
        Draw the current and best scores on the screen.
        
        Args:
            current_score (int): The current score.
            best_score (int): The best score.
        """
        self.score_screen.fill(self.graphical_board.bg_color)
        text_surface = self.font.render(f"Score: {current_score} Best: {best_score}", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.score_screen.get_rect().center)
        self.score_screen.blit(text_surface, text_rect)
    
    def reset_game(self):
        """
        Reset the game to its initial state by resetting the current score and the board.
        """
        self.current_score = 0
        
        self.board.reset() 

    def draw_game_over(self): 
        """
        Draw the game over screen with the best score and instructions to replay or quit.
        """
        self.score_screen.fill(self.graphical_board.bg_color)
        small_font = pygame.font.Font(None, 24)
        text_surface = small_font.render(f"Best Score: {self.best_score}; 'r' to replay, 'q' to quit", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.score_screen.get_rect().center)
        self.score_screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    def game_loop(self):
        """
        The main game loop that handles the game's runtime logic, including event handling, 
        updating game state, and rendering the game.
        This method runs continuously until the game is quit or the player loses. It processes 
        user inputs, updates the game state, and renders the game at a consistent frame rate.
        Attributes:
            running (bool): A flag to control the main game loop.
            direction_input_queue (list): A queue to store direction inputs from the player.
        Event Handling:
            - pygame.QUIT: Exits the game.
            - pygame.KEYDOWN: Handles directional inputs (up, down, left, right) and game reset (r) or quit (q) commands.
        Game State Updates:
            - Updates the direction of the snake based on the input queue.
            - Moves the snake and checks for collisions or food consumption.
            - Updates the current score and best score.
        Rendering:
            - Draws the current score and best score on the screen.
            - Draws the game over screen if the game is over.
        Game Over Handling:
            - Waits for the player to either quit the game (q) or reset the game (r).
        Returns:
            None
        """
        
        running = True
        direction_input_queue = [ ] 
        
        while running:                    
            
            self.draw_score(self.current_score, self.best_score)    
            delta_time = self.clock.tick() / 1000.0 

            
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_UP:
                        direction_input_queue.append("up")
                    elif event.key == pygame.K_DOWN:
                        direction_input_queue.append("down")
                    elif event.key == pygame.K_LEFT:
                        direction_input_queue.append("left")
                    elif event.key == pygame.K_RIGHT:
                        direction_input_queue.append("right")
                        
            while direction_input_queue:                
                direction_input = direction_input_queue.pop(0)
                if self.board.set_direction(direction_input):
                    break
                    
            over, eaten = self.graphical_board.move(delta_time)
            if eaten:
                self.current_score += 1
                
            self.best_score = max(self.best_score, self.current_score)

            if over:
                self.draw_game_over()
                condition = True
                
                while condition: 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                            condition = False
                            running = False
                            break
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            print("reset")
                            self.reset_game()
                            condition = False
                            break   




rows = 20
cols = 20
obstacles = [(1,2)]
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        import json
        json_input = json.load(f)
        rows = json_input["rows"]   
        cols = json_input["cols"]
        obstacles = json_input["obstacles"]

game = Game(rows, cols, obstacles,20,250,(30, 30, 30),(50, 50, 50),(0, 255, 0),(255, 0, 0))
game.start_game()