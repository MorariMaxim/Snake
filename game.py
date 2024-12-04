import sys
from Board import *
from GraphicalBoard import *
import pygame
class Game:
            
    def __init__(self, board_rows, board_columns, board_obstacles, block_size, snake_speed, bg_color, grid_color, snake_color, food_color) -> None:
                
        self.board = Board(board_rows, board_columns, board_obstacles)
        
        self.score = 0
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        self.graphical_board = GraphicalBoard(self.board, block_size, snake_speed, bg_color, grid_color, snake_color, food_color, self.clock, self.frame_rate)
        
    def start_game(self):
        
        self.board.set_direction((0, 1))
        
        self.game_loop()

    def game_loop(self):
        
        pygame.init()
        running = True
                
        while running:                    
            
            delta_time = self.clock.tick(self.frame_rate) / 1000.0      

            
                
            last_direction_input = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:                
                    if event.key == pygame.K_UP:
                        last_direction_input = "up"                        
                    elif event.key == pygame.K_DOWN:
                        last_direction_input = "down"
                    elif event.key == pygame.K_LEFT:
                        last_direction_input = "left"
                    elif event.key == pygame.K_RIGHT:
                        last_direction_input = "right"
            
            if last_direction_input:
                self.board.set_direction(last_direction_input)
     
            over, eaten = self.graphical_board.move(delta_time)

            if over:
                running = False
                


game = Game(10,10, [],20,200,(30, 30, 30),(50, 50, 50),(0, 255, 0),(255, 0, 0))
game.start_game()
