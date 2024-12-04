import pygame
from Board import Board

class GraphicalBoard():

    def __init__(self, board: Board, block_size, snake_speed, bg_color, grid_color, snake_color, food_color, screen, clock, frame_rate ) -> None:
        self.board = board
        self.block_size = block_size
        self.snake_speed = snake_speed
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.snake_color = snake_color
        self.food_color = food_color
        self.screen = screen
        self.clock = clock
        self.frame_rate = frame_rate
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.obstacle_color = (0, 0, 255)
                
        self.head_velocity = [0, 0]
        self.tail_velocity = [0, 0]
 
        
    def draw_grid(self):
        for row in range(self.board.rows):
            pygame.draw.line(self.screen, self.grid_color, (0, row * self.block_size), (self.screen_width, row * self.block_size))
        for col in range(self.board.columns):
            pygame.draw.line(self.screen, self.grid_color, (col * self.block_size, 0), (col * self.block_size, self.screen_height))
            
    def move(self, delta_time):
        self.head = [self.board.head.x * self.block_size, self.board.head.y * self.block_size]
        self.tail = [self.board.tail.x * self.block_size, self.board.tail.y * self.block_size]
        
        over, eaten = self.board.move()
                        
        # if over:
        #     return over, eaten
        
        self.set_velocities()
        
        self.move_snake()
        
        
        return over, eaten
    
    def set_velocities(self):
        self.head_velocity = [num * self.snake_speed for num in self.board.direction]
        
        tail_direction = [ self.board.tail.x - (self.tail[0] // self.block_size) ,  self.board.tail.y - (self.tail[1] // self.block_size)]
        self.tail_velocity = [num * self.snake_speed for num in tail_direction]

    def draw_food(self):
        pygame.draw.rect(self.screen, self.food_color, (self.board.food_position[0] * self.block_size, self.board.food_position[1] * self.block_size, self.block_size, self.block_size))    

    def draw_obstacles(self):
        for obstacle in self.board.obstacles:
            pygame.draw.rect(self.screen, self.obstacle_color, (obstacle[0] * self.block_size, obstacle[1] * self.block_size, self.block_size, self.block_size))
    
    def move_snake(self):  
        head_target = [self.board.head.x * self.block_size, self.board.head.y * self.block_size]        
        tail_target = [self.board.tail.x * self.block_size,self.board.tail.y * self.block_size]
        
        while True:
            delta_time = self.clock.tick(self.frame_rate) / 1000.0
            # print(self.head, self.tail)
            # print(self.head_velocity, self.tail_velocity)
            def helper(velocity, position, target):
                if velocity[0] != 0:  
                    position[0] += velocity[0] * delta_time
                    if (velocity[0] > 0 and position[0] >= target[0]) or (velocity[0] < 0 and position[0] <= target[0]):
                        position[0] = target[0]
                if velocity[1] != 0:  
                    position[1] += velocity[1] * delta_time
                    if (velocity[1] > 0 and position[1] >= target[1]) or (velocity[1] < 0 and position[1] <= target[1]):
                        position[1] = target[1]
                                    
            helper(self.tail_velocity, self.tail, tail_target)
            helper(self.head_velocity, self.head, head_target) 
            

            self.screen.fill(self.bg_color)          
            self.draw_grid()
            self.draw_food()
            self.draw_obstacles()
            pygame.draw.rect(self.screen, self.snake_color, (self.tail[0], self.tail[1], self.block_size, self.block_size))

            current = self.board.tail

            while current != self.board.head:
                pygame.draw.rect(self.screen, self.snake_color, (current.x * self.block_size, current.y * self.block_size, self.block_size, self.block_size))
                current = current.next
            
            pygame.draw.rect(self.screen, self.snake_color, (self.head[0], self.head[1], self.block_size, self.block_size))
            pygame.display.flip()
            
            if self.head[0] == head_target[0] and self.head[1] == head_target[1]:
                break
            
                