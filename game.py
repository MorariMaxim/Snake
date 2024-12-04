import sys
from Board import *
from GraphicalBoard import *
import pygame
class Game:
            
    def __init__(self, board_rows, board_columns, board_obstacles, block_size, snake_speed, bg_color, grid_color, snake_color) -> None:
                
        self.board = Board(board_rows, board_columns, board_obstacles)
        
        self.score = 0
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        self.graphical_board = GraphicalBoard(self.board, block_size, snake_speed, bg_color, grid_color, snake_color, self.clock, self.frame_rate)
        
    def start_game(self):
        
        self.board.set_direction((0, 1))
        

    def game_loop(self):
        
        pygame.init()
        running = True
                
        while running:                    
            
            delta_time = self.clock.tick(self.frame_rate) / 1000.0      

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:                
                    if event.key == pygame.K_UP:
                        self.board.set_direction("up")
                    elif event.key == pygame.K_DOWN:
                        self.board.set_direction("down")
                    elif event.key == pygame.K_LEFT:
                        self.board.set_direction("left")
                    elif event.key == pygame.K_RIGHT:
                        self.board.set_direction("right")
                        
            over, eaten = self.graphical_board.move(delta_time)

            if over:
                running = False                