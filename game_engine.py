import pygame
import game_mechanics
import random
import numpy as np
import math


class Col:
    """Defines all used colours"""
    def __init__(self):
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.red=(255,0,0)
        
        self.yellow=(255,255,0)
        self.green=(0,150,0)
        self.blue=(0,0,255)
        self.purple=(155,0,255)
        self.cyan=(0,255,255)
        self.grey=(150,150,120)
        self.pink=(255,120,120)
        self.darkgreen=(0,100,0)
        self.brown=(140,42,42)
        self.darkred=(50,0,0)
        self.darkgrey=(60,60,60)
        
        
        
c=Col()

class Tile:
    def __init__(self,c):
        self.empty=["Empty",c.white,1]
        self.sea=["Sea",c.blue,0]
        self.land=["Land",c.green,2]
        self.mountain=["Mountain",c.darkgrey,10]
        self.forest=["Forest",c.darkgreen,8]
        self.house=["House",c.yellow,3]
        self.woodcutter=["Woodcutter",c.brown,4]
        self.sealover=["Poseidon",c.cyan,5]
        self.mordor=["Mordor",c.darkred,9]
        self.darklord=["Dark Lord",c.black,11]
        
t=Tile(c)

      

class Position:
    def __init__(self,position):
        self.position=position
        self.x=position[0]
        self.y=position[1]
    def distance(self,diff_position):
        return(math.hypot(self.x-diff_position.x,self.y-diff_position.y))
    
class Rectangle(Position):
    def __init__(self,position,size):
        super().__init__(position)
        self.size = size #list of two values
    def width(self):
        return(self.size[0]) 
    def height(self):
        return(self.size[1])
    
class Window(Rectangle):
    def __init__(self,size,position=[0,0],bg_color=c.black):
        super().__init__(position,size)
        self.bg_color=bg_color
        self.screen = pygame.display.set_mode(self.size)
        
    def initialize_game(self):    
        pygame.init()
        pygame.display.set_caption("Dominikova hra")
        clock=pygame.time.Clock()
        self.screen.fill(self.bg_color)
        gameIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(gameIcon)
        return(clock)  

    def draw_ctverec(self,ctverec):
        x=ctverec[0]
        y=ctverec[1]
        sx=ctverec[2]
        sy=ctverec[3]
        color=ctverec[4]
        w=ctverec[5]
        pygame.draw.rect(self.screen,
                                 color,
                                 [x, y, sx, sy],w)
      
    def draw_grid(self,grid):
        for row in range(grid.rows):
            for column in range(grid.columns):
                value=grid.grid[row][column]
                color = grid.colors[value]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0],
                                  (grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1],
                                  grid.cell_size[0],
                                  grid.cell_size[1]])      
    
    def draw_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, label.color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
        
    def remove_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, self.bg_color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
    
class Grid(Rectangle):
    def __init__(self,rows,columns,position=[0,0],cell_size=[20,20],margin=1,colors=[c.green]):
        size=[(cell_size[0]+margin)*columns+margin,(cell_size[1]+margin)*columns+margin]
        super().__init__(position,size)
        self.colors=colors
        self.cell_size=cell_size
        self.margin=margin
        self.rows=rows
        self.columns=columns
        self.grid = []
        for row in range(rows):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(columns):
                self.grid[row].append(0)  # Append a cell 
                

    def get_element_index(self,row,column):
        if not(column>=self.columns or row>=self.rows or column<0 or row<0):
            row_len=self.columns
            #print(row,column,self.columns)
            index=row_len*row+column
            return(index)
                
    def evaluate_row_column_indices(self,click):
        column = (click[0]-self.position[0]) // (self.cell_size[0] + self.margin)
        row = (click[1]-self.position[1]) // (self.cell_size[1] + self.margin)
        return(row,column)
        #print(row,column)
    
    def empty_map(self):
        for i in range(self.rows):
            for j in range(self.columns):                 
                self.grid[i][j]=1
                
    def generate_random_map(self,terrains,*args):
            
        if len(args)>0:
            conditionterrain=args[0]
            #print (conditionterrain)
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.grid[i][j]==conditionterrain:
                        self.grid[i][j]=random.choice(terrains)
        elif len(args)==0:
            for i in range(self.rows):
                for j in range(self.columns):                 
                    self.grid[i][j]=random.choice(terrains)
            for i in range(self.rows):
                    self.grid[i][0]=0
                    self.grid[i][self.columns-1]=0
            for j in range(self.columns):
                    self.grid[0][j]=0 
                    self.grid[self.rows-1][j]=0
        
    def smooth_map_connector(self,value):
        mask=np.array(np.zeros((self.rows,self.columns),dtype=int))
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):                 
                if self.grid[i][j]==value:
                    
                   for k in range(i-1,i+1):#diagonalne
                       for l in range(j-1,j+1):
                          if self.grid[k][l]==value: 
                                mask[k][l]=1
                                mask[i][l]=1
                                mask[k][j]=1
                                mask[i][j]=1
                                
                    #horizontalne a vertikalne
                          if self.grid[i-1][j]==value and self.grid[i][j]==value and self.grid[i+1][j]==value: 
                                mask[i-1][j]=1
                                mask[i][j]=1
                                mask[i+1][j]=1
                                mask[i][j+1]=1
                                mask[i][j-1]=1
                          if self.grid[i][j-1]==value and self.grid[i][j]==value and self.grid[i][j+1]==value: 
                                mask[i][j-1]=1
                                mask[i][j]=1
                                mask[i][j+1]=1
                                mask[i-1][j]=1
                                mask[i+1][j]=1      
                            
                                
                
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):       
                if mask[i][j]==1:
                    self.grid[i][j]=value
                  #  self.grid[i+1][j]=value
                   # self.grid[i][j+1]=value 
                   
    def smooth_map_deletor(self,value,changevalue):
        mask=np.array(np.zeros((self.rows,self.columns),dtype=int))
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):                 
                if self.grid[i][j]==value: 
                   if self.grid[i-1][j-1]!=value and self.grid[i][j-1]!=value and self.grid[i+1][j-1]!=value and self.grid[i-1][j]!=value and self.grid[i+1][j]!=value and self.grid[i-1][j+1]!=value and self.grid[i][j+1]!=value and self.grid[i+1][j+1]!=value:
                      mask[i][j]=1                  
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):       
                if mask[i][j]==1:
                    self.grid[i][j]=changevalue
                  #  self.grid[i+1][j]=value
                   # self.grid[i][j+1]=value 
                   
    def smooth_map_differentiator(self,value,changevalue,probability):
        mask=np.array(np.zeros((self.rows,self.columns),dtype=int))
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):
                if self.grid[i][j]==value:                 
                    if self.grid[i-1][j-1]==value and self.grid[i][j-1]==value and self.grid[i+1][j-1]==value and self.grid[i-1][j]==value and self.grid[i+1][j]==value and self.grid[i-1][j+1]==value and self.grid[i][j+1]==value and self.grid[i+1][j+1]==value:
                        mask[i][j]=1
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):
                nahoda=random.randint(0,100)
                if mask[i][j]==1 and nahoda<probability:
                    self.grid[i][j]=changevalue
                  
                
                     
    def connect_map(self,value):#dominikova redundance
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):                 
                if self.grid[i+1][j]==value and self.grid[i-1][j]==value:
                    self.grid[i][j]=value
                    #self.grid[i][j+1]=value
                    #self.grid[i][j-1]=value
                if self.grid[i][j+1]==value and self.grid[i][j-1]==value:
                    self.grid[i][j]=value  
                    #self.grid[i-1][j]=value  
                    #self.grid[i+1][j]=value  

class MenuGrid(Grid):
    def __init__(self,rows,columns,position=[0,0],cell_size=[20,20],margin=1, colors=[c.white]):
        super().__init__(rows,columns,position,cell_size,margin,colors)
        #self.function_array=function_array
        #self.parameter_array=parameter_array
        
        
 
class Label(Position):
    def __init__(self,position,text,color=(0,0,0),font="Cambria",fontsize=10):
        super().__init__(position)
        self.text=text
        self.color=color
        self.font=font
        self.fontsize=fontsize

     

        
def main_program_loop(window,clock):
    done = False
    grids=[]
    labels=[]
    ctverce=[]
    grids=game_mechanics.initialize_grids(grids)
    labels=game_mechanics.initialize_labels(labels)
    ctverce=game_mechanics.initialize_ctverce(ctverce, grids)
    time_fr=0 #1/60 sec
    time=0 #1 sec
    #gameIcon = pygame.image.load('icon.png')
    #window.screen.blit(gameIcon,(10,10))
    while not done:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game_mechanics.evaluate_click(grids,pos,t,ctverce)                        
        window.screen.fill(window.bg_color)
        for grid in grids:
            window.draw_grid(grid)
        for label in labels:
            window.draw_label(label)
        for ctverec in ctverce:
            window.draw_ctverec(ctverec) 
                 
        
        clock.tick(60)
        
        time_fr+=1
        if time_fr%5==0:
            game_mechanics.update_labels(labels)
            game_mechanics.update_ctverce(ctverce)
            game_mechanics.time_event(grids,time_fr)
            #if time_fr>10:
            #    print (grids[0].grid[0][0])
        if time_fr%60==0:
            time+=1
            print("time:",time)
            
            
        pygame.display.flip()   
        

def run():
    window=Window([1400,700])
    clock = window.initialize_game()
    main_program_loop(window, clock)
    pygame.quit()
    

run()