import random


class Game:
    
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
            
        def set_direction(self, direction):
            
            self.direction = direction

        def move(self):
            
            if self.head.x + self.direction[0] < 0 or self.head.x + self.direction[0] >= self.rows or \
                self.head.y + self.direction[1] < 0 or self.head.y + self.direction[1] >= self.columns or\
                self.matrix[self.head.x + self.direction[0]][self.head.y + self.direction[1]] == -1:
                return False, None
            
            self.head.x += self.direction[0]
            self.head.y += self.direction[1] 
            
            eaten = False
            if self.matrix[self.head.x][self.head.y] == 2:
                eaten = True
                self.place_food()
                
                
            
            self.matrix[self.head.x][self.head.y] = 1
            
            return True, eaten
            
        def place_food(self):
            
            while True:
                random_x = random.randint(0, self.rows - 1)
                random_y = random.randint(0, self.columns - 1)
                
                if self.matrix[random_x][random_y] == 0:
                    self.matrix[random_x][random_y] = 2
                    break
        
    def __init__(self, board_rows, board_columns, board_obstacles) -> None:
                
        self.board = Game.Board(board_rows, board_columns, board_obstacles)                  