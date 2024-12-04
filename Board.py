import random

class Board:
        
    class Node:
        def __init__(self, x, y, next = None) -> None:
            self.x = x
            self.y = y
            self.next = next

    def __init__(self, rows, columns, obstacles) -> None:
        
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.direction = [0, 0]
        self.create_board()
        self.place_food()
        self.snake_length = 1
        self.create_linked_list()

    def reset(self):
        self.create_board()
        self.place_food()
        self.snake_length = 1
        self.create_linked_list()
        self.direction = [0, 0]
    
    def create_board(self):
        
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        
        for each_obstacle in self.obstacles:
            self.matrix[each_obstacle[1]][each_obstacle[0]] = -1 # -1 for obstacles
            
        # -1 for obstacles, 0 for empty spaces, 1 for snake, 2 for food

    def create_head(self):

        self.head = self.Node(self.columns//2, self.rows//2)

    def create_linked_list(self):
        
        self.create_head()
        self.tail = self.head
        self.tail.next = self.head  
            
    def set_direction(self, direction):
        
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
        if direction == "up" and self.direction[1] == 0 or\
            direction == "down" and self.direction[1] == 0 or\
            direction == "left" and self.direction[0] == 0 or\
            direction == "right" and self.direction[0] == 0:
            return True
        return False

    def move(self):
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
        
        while True:
            random_x = random.randint(0, self.columns - 1)
            random_y = random.randint(0, self.rows - 1)
            
            if self.matrix[random_y][random_x] == 0:
                self.food_position = [random_x, random_y]
                self.matrix[random_y][random_x] = 2
                break
