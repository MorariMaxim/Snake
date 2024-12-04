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
        direction_input_queue = []
            
        while running:                    
            
            delta_time = self.clock.tick(self.frame_rate) / 1000.0      

            
                
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

            if over:
                while running: 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                            running = False
                            break
                running = False 
                


game = Game(20, 20, [],20,300,(30, 30, 30),(50, 50, 50),(0, 255, 0),(255, 0, 0))
game.start_game()