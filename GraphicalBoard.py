import pygame
from Board import Board

class GraphicalBoard:
    """
    A class to represent the graphical board of the Snake game.
    """
    
    def __init__(self, board: Board, block_size, snake_speed, bg_color, grid_color, snake_color, food_color, screen) -> None:
        """
        Initialize the graphical board with the given parameters.
        
        Args:
            board (Board): The logical game board.
            block_size (int): Size of each block in pixels.
            snake_speed (int): Speed of the in pixels per second.
            bg_color (tuple): Background color.
            grid_color (tuple): Grid color.
            snake_color (tuple): Snake color.
            food_color (tuple): Food color.
            screen (pygame.Surface): The grid surface. 
        """
        self.board = board
        self.block_size = block_size
        self.snake_speed = snake_speed
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.snake_color = snake_color
        self.food_color = food_color
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.obstacle_color = (0, 0, 255)
                
        self.head_velocity = [0, 0]
        self.tail_velocity = [0, 0]
 
        pygame.mixer.init()  
        self.eat_sound = pygame.mixer.Sound("eat_sound.wav")
        
    def draw_grid(self):
        """
        Draw the grid on the screen by drawing horizontal and vertical lines.
        """
        for row in range(self.board.rows):
            pygame.draw.line(self.screen, self.grid_color, (0, row * self.block_size), (self.screen_width, row * self.block_size))
        for col in range(self.board.columns):
            pygame.draw.line(self.screen, self.grid_color, (col * self.block_size, 0), (col * self.block_size, self.screen_height))
            
    def move(self):
        """
        Move the snake and update the game state.
         
        Returns:
            tuple: A tuple containing a boolean indicating if the game is over and a boolean indicating if food was eaten.
        """
        self.head = [self.board.head.x * self.block_size, self.board.head.y * self.block_size]
        self.tail = [self.board.tail.x * self.block_size, self.board.tail.y * self.block_size]
        
        over, eaten = self.board.move()
        
        self.set_velocities()
        
        self.move_snake()
        
        if eaten:
            self.eat_sound.play()
        
        return over, eaten
    
    def set_velocities(self):
        """
        Set the velocities of the snake's head and tail based on the current direction and tail's next node.
        """
        self.head_velocity = [num * self.snake_speed for num in self.board.direction]
        
        tail_direction = [ self.board.tail.x - (self.tail[0] // self.block_size) ,  self.board.tail.y - (self.tail[1] // self.block_size)]
        self.tail_velocity = [num * self.snake_speed for num in tail_direction]

    def draw_food(self):
        """
        Draw the food on the screen at the current food position.
        """
        pygame.draw.rect(self.screen, self.food_color, (self.board.food_position[0] * self.block_size, self.board.food_position[1] * self.block_size, self.block_size, self.block_size))    

    def draw_obstacles(self):
        """
        Draw the obstacles on the screen at their respective positions.
        """
        for obstacle in self.board.obstacles:
            pygame.draw.rect(self.screen, self.obstacle_color, (obstacle[0] * self.block_size, obstacle[1] * self.block_size, self.block_size, self.block_size))
    
    def move_snake(self):          
        """  
        This method continuously updates the position of the snake's head and tail based on their respective velocities.
        It calculates the new positions using the elapsed time since the last frame and ensures that the head and tail
        move towards their target positions. The method also handles the rendering of the snake, the grid, food, and obstacles
        on the screen.
        The movement is controlled by a helper function that adjusts the position of the head and tail based on their velocities.
        The method runs in a loop until the head reaches its target position.
        Attributes:
            head_target (list): The target position for the snake's head in pixels.
            tail_target (list): The target position for the snake's tail in pixels.
            delta_time (float): The time elapsed since the last frame in seconds.
            helper (function): A nested function that updates the position of a given part of the snake based on its velocity.
            current (Node): A reference to the current segment of the snake being drawn.
        The method performs the following steps:
            1. Calculate the target positions for the head and tail.
            2. Enter a loop that continues until the head reaches its target position.
            3. Calculate the elapsed time since the last frame.
            4. Update the positions of the head and tail using the helper function.
            5. Clear the screen and redraw the grid, food, obstacles, and snake.
            6. Update the display with the new frame.
            7. Break the loop if the head reaches its target position.  
        """
        
        head_target = [self.board.head.x * self.block_size, self.board.head.y * self.block_size]        
        tail_target = [self.board.tail.x * self.block_size,self.board.tail.y * self.block_size]
        
        while True:
            delta_time = self.clock.tick() / 1000.0
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

