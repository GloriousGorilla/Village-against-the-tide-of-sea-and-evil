import game_engine
import pygame
import random
from collections import Counter
import math

class memory():
    def __init__(self, value,gold=0,wood=0,food=0,inh=10,time=0,life=0,used_inh=0):
        self.value=value
        self.gold=gold
        self.wood=wood
        self.food=food
        self.inh=inh
        self.time=time
        self.life=life
        self.used_inh=used_inh
        self.busy_buildings=[]
        self.busy_farms=[]
        self.busy_buildings3=[]
        self.row=[]
        self.column=[]
        self.tiletype=[]
        self.tiletypename=[]
mem=memory(3,10000,10000,50,10,0,0,0)


def initialize_grids(grids):
    c=game_engine.Col()
    t=game_engine.Tile(c)
    grids.append(game_engine.Grid(29,45,position=[15,55],colors=[t.sea[1],t.empty[1],t.land[1],t.house[1],t.woodcutter[1],t.sealover[1],c.red,c.white,t.forest[1],t.mordor[1],t.mountain[1],t.darklord[1]]))
    terrains=[1]
    grids[0].empty_map()
    grids.append(game_engine.Grid(6,1,position=[1185,380],cell_size=[200,25],margin=5,colors=[c.grey,c.green]))
    grids.append(game_engine.Grid(10,1,position=[1185,50],cell_size=[200,25],margin=5,colors=[c.grey,c.green]))   
    grids.append(game_engine.Grid(10,1,position=[975,50],cell_size=[200,25],margin=5,colors=[c.white]))
    grids.append(game_engine.Grid(3,1,position=[1185,590],cell_size=[200,25],margin=5,colors=[c.grey]))
    return(grids)

def initialize_ctverce(ctverce,grids):
    ctverce.append([grids[1].margin + grids[1].position[0],
                    grids[1].margin + grids[1].position[1],
                    grids[1].cell_size[0],
                    grids[1].cell_size[1],
                    (255,0,0),
                        2])
                        
    return(ctverce)

def initialize_labels(labels):
    menu1=["Nothing", "Build a house (200)","Build a woodcutter (500)", "Place Poseidon (1000)", "Place Dark Lord (1000)", "", "", "Coordinates: ", "Tile type: ", ""]
    for i in range(len(menu1)):    
        labels.append(game_engine.Label([1200,387+30*i],menu1[i],fontsize=15))
        
    menu2=["Reset","Generate Terrain","Smooth Terrain","Plant Trees","", "", "", "", "", "100 Food->1 Inhabitant"]
    for i in range(len(menu2)):    
        labels.append(game_engine.Label([1200,57+30*i],menu2[i],fontsize=15))
 
    menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Time: "+str(mem.time),"Inhabitants: "+str(mem.inh-mem.used_inh)+"/"+str(mem.inh), "Life: "+str(mem.life), "", "", "", ""]    
    for i in range(len(menu3)):    
        labels.append(game_engine.Label([990,57+30*i],menu3[i],fontsize=15)) #620
        
    headlabelmenu1=["BUILD:"]
    labels.append(game_engine.Label([1200,365],headlabelmenu1[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu2=["MAP EDITOR:"]
    labels.append(game_engine.Label([1200,35],headlabelmenu2[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu3=["GAME VARIABLES:"]
    labels.append(game_engine.Label([990,35],headlabelmenu3[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu4=["TILE INFO:"]
    labels.append(game_engine.Label([1200,575],headlabelmenu4[0],color=(255,255,255),fontsize=15))
    
    headlabelmap=["MAP:"]
    labels.append(game_engine.Label([30,35],headlabelmap[0],color=(255,255,255),fontsize=15))
        
    return(labels)

def evaluate_click(grids,click,t,ctverce):
    map_grids=[grids[0]]
    menu_grids=[grids[1],grids[2]]
    tlist=[t.empty, t.sea, t.land, t.house, t.woodcutter, t.mountain, t.forest, t.sealover, t.mordor, t.darklord]
    tlist_value=[item[2] for item in tlist]
    for grid in map_grids:
        row,column=grid.evaluate_row_column_indices(click)
        set_element_value(grid,row,column,mem.value)  
        #print("Click ", click, "Grid coordinates: ", row, column)#######################
        if row>=0 and row<=28 and column>=0 and column<=44:
            mem.row=row
            mem.column=column
            mem.tiletype=grid.grid[row][column]
            
            
            
            
            #mem.tiletypename=[i for i,x in enumerate([tlist[1][2],tlist[2][2],tlist[3][2],tlist[4][2],tlist[5][2]) if x==mem.tiletype]
            # => [1, 3]
            hledanyindex=tlist_value.index(mem.tiletype) 
            mem.tiletypename=(tlist[hledanyindex][0])
        else:
            mem.row=". "
            mem.column=" ."
            mem.tiletypename="None"
           
        
    for grid in menu_grids:

        row,column=grid.evaluate_row_column_indices(click)
        
        index=grid.get_element_index(row,column)
        if index is not None:
            if grid==grids[1]:
                function_array=[set_value,set_value,set_value,set_value,set_value,nothing, nothing]
                parameter_array=[0,3,4,5,11,0,0]
            elif grid==grids[2]:
                function_array=[reset,generate_terrain,smooth_terrain,plant_trees,nothing,nothing,nothing,nothing,nothing,add_inhabitant]
                parameter_array=[grids[0],grids[0],grids[0],grids[0],20]
                   
                
            if row<=grid.rows and row>=0 and column<=grid.columns and column>=0:
                ctverce[0][0]=(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0]
                ctverce[0][1]=(grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1]
                ctverce[0][2]=grid.cell_size[0]
                ctverce[0][3]=grid.cell_size[1]
            
            function_array[index](parameter_array[index])
        
            print(row, column)
        
                

def nothing(x):
    pass

def reset(grid):
    terrains=[1]
    grid.generate_random_map(terrains)
    mem.food=50
    mem.gold=10000
    mem.wood=10000
    mem.time=0
    mem.life=0
    mem.inh=10
    mem.used_inh=0
    mem.value=3
    
def generate_terrain(grid):
    terrains=[0,0,0,0,0,0,0,0,2,2,2,2,2]
    grid.generate_random_map(terrains)
    
def plant_trees(grid):
    terrains=[8,2,2,2,2,2]
    grid.generate_random_map(terrains,2)
    
    
def smooth_terrain(grid):
    #grid.smooth_map(0)
    #grid.smooth_map(2)
    grid.smooth_map_deletor(2,0)
    grid.smooth_map_connector(2)
    grid.smooth_map_differentiator(2,10,20)
    grid.smooth_map_connector(10)
def add_inhabitant(value):
    if mem.food>=100:
        mem.inh+=1
        mem.food-=100
    
def set_value(value):
    mem.value=value
    #print (value)
    
def turn(x):
    mem.gold=mem.gold+x
    
    

 
def check_resources(value):
    if value==3 and mem.wood>=200 and mem.inh-mem.used_inh>=0:
        return(True)
    elif value==4 and mem.wood>=500 and mem.inh-mem.used_inh>=0:
        return(True)
    elif value==5 and mem.wood>=1000 and mem.inh-mem.used_inh>=0:
        return(True)
    elif value==11 and mem.wood>=1000 and mem.inh-mem.used_inh>=0:
        return(True)
    elif value==6 or value==7:
        return(True)
    
    else:
        return(False)

def pay_resources(value):
    if value==3:
        mem.wood-=200
        mem.used_inh+=0
    elif value==4:
        mem.wood-=500
        mem.used_inh+=0
    elif value==5:
        mem.wood-=1000
        mem.used_inh+=0
    elif value==11:
        mem.wood-=1000
        mem.used_inh+=0

    
def set_element_value(grid,row,column,value,clicked=True):
    if not(column>=grid.columns or row>=grid.rows or column<0 or row<0):
        if grid.grid[row][column] not in [0,1,3,4,5,6,8,9,10,11]: #stavění
            enough_resources=check_resources(value)
            if enough_resources:
                pay_resources(value)
                grid.grid[row][column] = value
                if value==4:
                    mem.busy_buildings.append(0) #busy woodcutters
                if value==5:
                    mem.busy_farms.append(0)
                if value==11:
                    mem.busy_buildings3.append(0)
        if grid.grid[row][column] in [6,8] and clicked: #klikání
            resource=grid.grid[row][column]
            grid.grid[row][column] = 2
            if resource==6:
                mem.food+=10
            if resource==8:
                mem.wood+=10
        if grid.grid[row][column] in [2] and clicked=="Sealover": #klikání
            resource=grid.grid[row][column]
            grid.grid[row][column] = 0
        if grid.grid[row][column] in [2] and clicked=="Mordor": #klikání
            resource=grid.grid[row][column]
            grid.grid[row][column] = 9
            #if resource==6:
            #    mem.food+=10
            #if resource==8:
            #    mem.wood+=10
        

def count_objects(grid):
    """Count occurence of given items"""
    flat_grid=[]
    for i in range(0,grid.rows):
        flat_grid+=grid.grid[i]
    occurence=Counter(flat_grid)
    return(occurence)

def increment_resources(occurence):
    houses=occurence[3]
    woodcutters=occurence[4]
    farms=occurence[5]
    building3 = occurence[9]
    """increment"""
    mem.gold+=houses
    mem.life-=building3
    if mem.gold>=4*farms+2*woodcutters:
        mem.gold-=4*farms
        mem.gold-=2*woodcutters
        #mem.food+=farms
        #mem.wood+=woodcutters

   
def time_event(grids,time_fr):
    if time_fr%5==0:
        grid=grids[0]
        random_resource(grid)       
    if time_fr%10==0:
        mem.time=mem.time+1
        mem.life=mem.life+1
        if mem.food>0:
            mem.food-=mem.inh
            mem.inh=mem.inh*(1+0.1/60)
        if mem.food<=0:
            mem.food=0
            mem.inh=mem.inh*0.9
            
        occurence=count_objects(grid)
        increment_resources(occurence)
        print(mem.busy_buildings)
        buildings_pos=find_buildings(grid,4) # drevorubec kácí
        near_distances,near_positions=find_nearest_resource(grid,8,buildings_pos,1000,1000)
        print(near_distances,near_positions,mem.busy_buildings)
        for i in range(len(mem.busy_buildings)):
            if mem.busy_buildings[i]==0:
                mem.busy_buildings[i]=5+math.floor(near_distances[i])
            elif mem.busy_buildings[i]==1:
                set_element_value(grid,near_positions[i].x,near_positions[i].y,2)
                mem.busy_buildings[i]-=1
            else:
                mem.busy_buildings[i]-=1
        print(mem.busy_buildings)
        
        
        
        buildings_pos=find_buildings(grid,5) #farmy (zeus) mizej
        near_distances,near_positions=find_nearest_resource(grid,2,buildings_pos,1000,1000) #cislo znaci kterej land hledam
        print(near_distances,near_positions,mem.busy_farms)
        for i in range(len(mem.busy_farms)):
            if mem.busy_farms[i]==0:
                mem.busy_farms[i]=5+math.floor(near_distances[i])
            elif mem.busy_farms[i]==1:
                set_element_value(grid,near_positions[i].x,near_positions[i].y,0, "Sealover") #posledni znaci na co se to zmeni
                mem.busy_farms[i]-=1
            else:
                mem.busy_farms[i]-=1
        print(mem.busy_farms)
        
        buildings_pos=find_buildings(grid,11) #mordor tmaví
        near_distances,near_positions=find_nearest_resource(grid,2,buildings_pos,9,11) #cislo znaci kterej land hledam
        print(near_distances,near_positions,mem.busy_buildings3)
        for i in range(len(mem.busy_buildings3)):
            if mem.busy_buildings3[i]==0:
                mem.busy_buildings3[i]=5+math.floor(near_distances[i])
            elif mem.busy_buildings3[i]==1:
                set_element_value(grid,near_positions[i].x,near_positions[i].y,9, "Mordor") #posledni znaci na co se to zmeni
                mem.busy_buildings3[i]-=1
            else:
                mem.busy_buildings3[i]-=1
        print(mem.busy_buildings3)
        
        
def find_buildings(grid,tile_value):
    buildings_pos=[]
    for row in range(grid.rows):
        for column in range(grid.columns):
            if grid.grid[row][column]==tile_value:
                buildings_pos.append(game_engine.Position([row,column]))
                
                
    return(buildings_pos)
    

def find_nearest_resource(grid,tile_value,positions,nexttile_value,building_value):
    
    near_distances=list(range(100,100+len(positions)))
    near_positions=list(range(100,100+len(positions)))
    for row in range(grid.rows):
        for column in range(grid.columns):
            if grid.grid[row][column]==tile_value:
                if nexttile_value != 1000: #a zaroven by se dalo rict ze building_value musi byt 1000 ale nastava to ve stejnych pripadech
                    if (grid.grid[row-1][column]==nexttile_value or grid.grid[row-1][column]==building_value or grid.grid[row+1][column]==nexttile_value or grid.grid[row+1][column]==building_value or grid.grid[row][column-1]==nexttile_value or grid.grid[row][column-1]==building_value or grid.grid[row][column+1]==nexttile_value or grid.grid[row][column+1]==building_value): #or grid.grid[row+1][column]==(nexttile_value or building_value) or grid.grid[row][column-1]==(nexttile_value or building_value) or grid.grid[row][column+1]==(nexttile_value or building_value):   
                        pos=game_engine.Position([row,column])
                        for i in range(len(positions)):
                            dist=pos.distance(positions[i])
                            if dist<near_distances[i]:
                                near_distances[i]=dist
                                near_positions[i]=pos 
                else:    
                    pos=game_engine.Position([row,column])
                    for i in range(len(positions)):
                        dist=pos.distance(positions[i])
                        if dist<near_distances[i]:
                            near_distances[i]=dist
                            near_positions[i]=pos
    return(near_distances,near_positions)
                    

    


def random_resource(grid):
    closearea=2
    counter=0
    row=random.randint(closearea,grid.rows-1-closearea)
    column=random.randint(closearea,grid.columns-1-closearea)
    for i in range(row-closearea,row+closearea+1):
        for j in range(column-closearea,column+closearea+1):
            if grid.grid[i][j]==8:
                counter=counter+1
    if counter!=0 and grid.grid[row][column]==2:
        #print (counter)
        grid.grid[row][column]=8
    counter=0
            
    #choice=random.choice([0,0,0,1])
    #if choice==0:
    #    set_element_value(grid,row,column,7,clicked=False) 
    #else:
    #    set_element_value(grid,row,column,6,clicked=False)
        
def update_ctverce(ctverce):
    #ctverce[0][2]+=5 
    print(ctverce[0])

def update_labels(labels):
    labels[20].text="Gold: "+str(round(mem.gold))
    labels[21].text="Wood: "+str(round(mem.wood))
    labels[22].text="Food: "+str(round(mem.food))
    labels[23].text="Time: "+str(round(mem.time))
    labels[24].text="Life: "+str(round(mem.life))
    labels[25].text="Inhabitants: "+str(round(mem.inh-mem.used_inh))+"/"+str(round(mem.inh))
    labels[7].text="Coordinates: "+str(mem.row)+","+str(mem.column)
    labels[8].text="Tile type: "+str(mem.tiletypename)
        #menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Inhabitants: "+str(mem.inhabitants)]    
    #for i in range(len(menu3)):    
     #   labels.append(game_engine.Label([1020,70+55*i],menu3[i],fontsize=20))