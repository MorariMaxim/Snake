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
        
        self.create_linked_list()

    def create_board(self):
        
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        
        for each_obstacle in self.obstacles:
            self.matrix[each_obstacle[0]][each_obstacle[1]] = -1 # -1 for obstacles
            
        # -1 for obstacles, 0 for empty spaces, 1 for snake, 2 for food

    def create_head(self):

        self.head = self.Node(self.rows//2, self.columns//2)

    def create_linked_list(self):
        
        self.create_head()
        self.tail = self.head
        self.tail.next = self.head  
        
    def set_direction(self, direction):
        
        if direction == "up" and self.direction[1] == 0:    
            self.direction = [0, -1]
        elif direction == "down" and self.direction[1] == 0:
            self.direction = [0, 1]
        elif direction == "left" and self.direction[0] == 0:
            self.direction = [-1, 0]
        elif direction == "right" and self.direction[0] == 0:
            self.direction = [1, 0]
                

    def move(self):
        
        if self.head.x + self.direction[0] < 0 or self.head.x + self.direction[0] >= self.rows or \
            self.head.y + self.direction[1] < 0 or self.head.y + self.direction[1] >= self.columns or\
            self.matrix[self.head.x + self.direction[0]][self.head.y + self.direction[1]] == -1:
            return True, None

        temp = self.head
        self.head = self.Node(self.head.x + self.direction[0], self.head.y + self.direction[1])
        temp.next = self.head
        
        eaten = False
        if self.matrix[self.head.x][self.head.y] == 2:
            eaten = True
            self.place_food()                                
        else:
            self.tail = self.tail.next
            if not self.tail.next:
                self.tail.next = self.head

        
        self.matrix[self.head.x][self.head.y] = 1
        
        return False, eaten
        
    def place_food(self):
        
        while True:
            random_x = random.randint(0, self.rows - 1)
            random_y = random.randint(0, self.columns - 1)
            
            if self.matrix[random_x][random_y] == 0:
                self.matrix[random_x][random_y] = 2
                break
