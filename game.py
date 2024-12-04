import sys
from Board import *
from GraphicalBoard import *
import pygame
class Game:
            
    def __init__(self, board_rows, board_columns, board_obstacles, block_size, snake_speed, bg_color, grid_color, snake_color, food_color) -> None:
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
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        grid_rect = pygame.Rect(0, self.score_height, self.screen_width, self.screen_height - self.score_height)
        self.board_screen = self.screen.subsurface(grid_rect)
        self.score_screen = self.screen.subsurface(pygame.Rect(0, 0, self.screen_width, self.score_height))
        
        self.board = Board(self.board_rows, self.board_columns, self.board_obstacles)
        self.graphical_board = GraphicalBoard(self.board, self.block_size, self.snake_speed, self.bg_color, self.grid_color, self.snake_color, self.food_color, self.board_screen, self.clock, self.frame_rate)
        
    def start_game(self):
        
        self.board.set_direction((0, 1))
        
        self.game_loop()

    def draw_score(self, current_score, best_score):
        self.score_screen.fill(self.graphical_board.bg_color)
        text_surface = self.font.render(f"Score: {current_score} Best: {best_score}", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.score_screen.get_rect().center)
        self.score_screen.blit(text_surface, text_rect)
    
    def reset_game(self):
        self.current_score = 0
        
        self.board.reset() 

        
    
    def game_loop(self):
        
        running = True
        direction_input_queue = [ ] 
        
        while running:                    
            
            self.draw_score(self.current_score, self.best_score)
            # delta_time = self.clock.tick(self.frame_rate) / 1000.0      
            delta_time = self.clock.tick() / 1000.0 

            
                
            initial_length = len(direction_input_queue)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_UP:
                        print("up")
                        direction_input_queue.append("up")
                    elif event.key == pygame.K_DOWN:
                        print("down")
                        direction_input_queue.append("down")
                    elif event.key == pygame.K_LEFT:
                        print("left")
                        direction_input_queue.append("left")
                    elif event.key == pygame.K_RIGHT:
                        print("right")
                        direction_input_queue.append("right")
            if initial_length != len(direction_input_queue):
                print('-'*10)
            while direction_input_queue:                
                direction_input = direction_input_queue.pop(0)
                if self.board.set_direction(direction_input):
                    break
                    
            over, eaten = self.graphical_board.move(delta_time)
            if eaten:
                self.current_score += 1
                
            self.best_score = max(self.best_score, self.current_score)

            if over:
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
                print("out")




rows = 20
cols = 20
obstacles = [(0,0), (5,5)]
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        import json
        json_input = json.load(f)
        rows = json_input["rows"]   
        cols = json_input["cols"]
        obstacles = json_input["obstacles"]

game = Game(rows, cols, obstacles,20,300,(30, 30, 30),(50, 50, 50),(0, 255, 0),(255, 0, 0))
game.start_game()