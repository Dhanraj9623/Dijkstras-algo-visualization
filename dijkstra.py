import pygame
import queue
clock = pygame.time.Clock()
WIDTH = 800
cell_size = 20

win = pygame.display.set_mode((WIDTH,WIDTH))

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)
GREY = (128,128,128)

class Node:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cell_size=cell_size
        self.color=WHITE
        self.neighbors = []
        self.distance = float('inf')
        self.explored = False
        self.came_from = None
    
    def get_pos(self):
        return self.x,self.y
    
    def is_explored(self):
        return self.color == GREEN
    
    def is_open(self):
        return self.color == RED
    
    def is_wall(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE    
    
    def is_end(self):
        return self.color == YELLOW
    
    def reset(self):
        self.color = WHITE
        
    def set_explored(self):
        self.color = RED
    
    def set_open(self):
        self.color = GREEN
    
    def set_wall(self):
        self.color = BLACK
    
    def set_start(self):
        self.color = ORANGE
        
    def set_end(self):
        self.color = YELLOW
        
    def set_path(self):
        self.color = BLUE
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x * cell_size,self.y * cell_size,self.cell_size,self.cell_size))
        pygame.draw.rect(win,GREY,(self.x * cell_size,self.y * cell_size,self.cell_size,self.cell_size),1)
        
    def update_neighbors(self, grid):
        #if x < total rows
        if self.x  < WIDTH // cell_size -1 and not grid[self.x  + 1][self.y].is_wall():       #down
            self.neighbors.append(grid[self.x  + 1][self.y ])
           
        if self.x  > 0 and not grid[self.x - 1][self.y ].is_wall():                           #up
            self.neighbors.append(grid[self.x - 1][self.y])
        
        if self.y  < WIDTH // cell_size   - 1 and not grid[self.x ][self.y  + 1].is_wall():   #right
            self.neighbors.append(grid[self.x][self.y  + 1])

        if self.y > 0 and not grid[self.x ][self.y - 1].is_wall():                            #left
            self.neighbors.append(grid[self.x][self.y - 1])

def dijkstra(grid,start,end):
    node = start 
    node.distance = 0
    myqueue = []
    myqueue.append(start)
    
    while node != end:
    
        
        for i in range (len(node.neighbors)):
            if(node.distance + 1 < node.neighbors[i].distance and ((node.neighbors[i].x,node.neighbors[i].y) != node.came_from)):
                node.neighbors[i].distance = node.distance + 1 
                myqueue.append(node.neighbors[i])
                node.neighbors[i].came_from = node.x,node.y
                print(node.neighbors[i].distance,node.neighbors[i].x,node.neighbors[i].y,node.neighbors[i].came_from)
                node.neighbors[i].set_open()
            
        node.explored = True
        if node != start:
            node.set_explored()
        myqueue.pop(0)
        draw(win, grid)  
        pygame.time.delay(1)
        node = myqueue[0]
        
        
        if node == None:
            break
    node = end
    while node !=start:
        draw(win, grid) 
        pygame.time.delay(1)
        a,b=node.came_from
        grid[a][b].set_path()
        node = grid[a][b]
    start.set_start()  
    end.set_end() 
       
def make_grid(rows):
    print(rows)
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j)
            grid[i].append(node)
    return grid


def draw(win, grid):
    win.fill(WHITE)
    
    
    for row in grid:
        
        for node in row:
            
            node.draw(win)
            
    pygame.display.update()

def main():
    #win.fill((255,255,255))
    grid = make_grid(WIDTH//cell_size)
    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         print(grid[i][j].x,grid[i][j].y,end=' ')
    #     print()
    
    start = None
    end = None 
    
    running = True
    while running:  
        
        draw(win,grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                node = grid[x//cell_size][y//cell_size]
                if start==None and node != end:
                    start = node
                    node.set_start()
                elif end == None and node !=start:
                    end = node
                    node.set_end()
                elif node !=start and node != end :
                    node.set_wall()
            elif pygame.mouse.get_pressed()[2]:
                x,y = pygame.mouse.get_pos()
                node = grid[x//cell_size][y//cell_size]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #grid[0][0].color = ORANGE
                    
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    # for i in range(WIDTH//cell_size):
                    #     for j in range(WIDTH//cell_size):
                    #         node = grid[i][j]
                    #         print(i,j,len(node.neighbors))
                    #     print()         
                    dijkstra(grid,start,end)
               
        pygame.display.flip() 
    pygame.quit()
    
main()