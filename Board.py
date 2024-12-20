import random

class Board:
    """
    A class to represent the logic of the game.
    """
    
    class Node:
        """
        A class to represent a node in the snake's body.
        """
        
        def __init__(self, x, y, next=None) -> None:
            """
            Initialize a node with the given coordinates and next node.
            
            Args:
                x (int): The x-coordinate.
                y (int): The y-coordinate.
                next (Node, optional): The next node. Defaults to None.
            """
            self.x = x
            self.y = y
            self.next = next

    def __init__(self, rows, columns, obstacles) -> None:
        """
        Initialize the board with the given parameters.
        
        Args:
            rows (int): Number of rows in the board.
            columns (int): Number of columns in the board.
            obstacles (list): List of obstacles on the board.
        """
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.direction = [0, 0]
        self.create_board()
        self.place_food()
        self.snake_length = 1
        self.create_linked_list()

    def reset(self):
        """
        Reset the board to its initial state by recreating the board, placing food, and resetting the snake.
        """
        self.create_board()
        self.place_food()
        self.snake_length = 1
        self.create_linked_list()
        self.direction = [0, 0]
    
    def create_board(self):
        """
        Create the game board matrix with obstacles.
        
        0: Empty
        1: Snake
        2: Food
        -1: Obstacle
        
        an obstacles is specified in the form of a tuple (y, x)
        """
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        
        for each_obstacle in self.obstacles:
            self.matrix[each_obstacle[1]][each_obstacle[0]] = -1 
        

    def create_head(self):
        """
        Create the head of the snake at the center of the board.
        """
        self.head = self.Node(self.columns//2, self.rows//2)

    def create_linked_list(self):
        """
        Create the linked list representing the snake's body with the head as the only node.
        """
        self.create_head()
        self.tail = self.head
        self.tail.next = self.head  
            
    def set_direction(self, direction):
        """
        Set the direction of the snake's movement.
        
        Args:
            direction (str): The direction to set ('up', 'down', 'left', 'right').
        
        Returns:
            bool: True if the direction is valid, False otherwise.
        """
        valid = self.validate_direction(direction)
        
        if direction == "up" and self.direction[1] == 0:    
            self.direction = [0, -1]
        elif direction == "down" and self.direction[1] == 0:
            self.direction = [0, 1]
        elif direction == "left" and self.direction[0] == 0:
            self.direction = [-1, 0]
        elif direction == "right" and self.direction[0] == 0:
            self.direction = [1, 0]
            
        return valid
    
    def validate_direction(self, direction):
        """
        Validate the direction of the snake's movement.
        
        Args:
            direction (str): The direction to validate ('up', 'down', 'left', 'right').
        
        Returns:
            bool: True if the direction is valid, False otherwise.
        """
        if direction == "up" and self.direction[1] == 0 or\
            direction == "down" and self.direction[1] == 0 or\
            direction == "left" and self.direction[0] == 0 or\
            direction == "right" and self.direction[0] == 0:
            return True
        return False

    def move(self):
        """
        Move the snake on the board.
        
        Returns:
            tuple: A tuple containing a boolean indicating if the game is over and a boolean indicating if food was eaten.
        """
        if self.direction == [0, 0]:
            return False, None
        
        if self.head.x + self.direction[0] < 0 or self.head.x + self.direction[0] >= self.columns or \
            self.head.y + self.direction[1] < 0 or self.head.y + self.direction[1] >= self.rows or\
            self.matrix[self.head.y + self.direction[1]][self.head.x + self.direction[0]] == -1 or\
            self.matrix[self.head.y + self.direction[1]][self.head.x + self.direction[0]] == 1:
            return True, None

        temp = self.head
        self.head = self.Node(self.head.x + self.direction[0], self.head.y + self.direction[1])
        temp.next = self.head
        
        eaten = False
        if self.matrix[self.head.y][self.head.x] == 2:
            eaten = True
            self.place_food()   
            self.snake_length += 1
        else:
            self.matrix[self.tail.y][self.tail.x] = 0
            self.tail = self.tail.next
            if not self.tail.next:
                self.tail.next = self.head

        
        self.matrix[self.head.y][self.head.x] = 1
        
        return False, eaten
        
    def place_food(self):
        """
        Place food on the board at a random empty position.
        """
        while True:
            random_x = random.randint(0, self.columns - 1)
            random_y = random.randint(0, self.rows - 1)
            
            if self.matrix[random_y][random_x] == 0:
                self.food_position = [random_x, random_y]
                self.matrix[random_y][random_x] = 2
                break
