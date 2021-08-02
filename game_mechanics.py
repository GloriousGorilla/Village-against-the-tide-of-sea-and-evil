import game_engine
import pygame
import random
from collections import Counter
import math

class memory():
    def __init__(self, value,gold=0,wood=0,food=0,inh=10,time=0,life=0,used_inh=0,alert="You are good",alertcounter=0, gameon=0, gameonstatus="OFF",gameonbuttoncounter=0,burnedforests=0):
        self.value=value
        self.gold=gold
        self.wood=wood
        self.food=food
        self.inh=inh
        self.time=time
        self.life=life
        self.used_inh=used_inh
        self.busy_buildings1=[] #cottage
        self.busy_buildings2=[] #woodcutter
        self.busy_buildings3=[] #poseidon
        self.busy_buildings4=[] #farm
        self.busy_buildings5=[] #townhall
        self.busy_buildings6=[] #druidtemple
        self.busy_natureevent1=[] #fires
        self.row=[]
        self.column=[]
        self.tiletype=[]
        self.tiletypename=[]
        self.alert=alert
        self.alertcounter=alertcounter
        self.gameon=gameon
        self.gameonstatus=gameonstatus
        self.gameonbuttoncounter=gameonbuttoncounter
        self.burnedforests=burnedforests
        self.listoffire_pos=[]
        self.tile_attractiveness_for_conversion=[]
        self.tile_protection_for_conversion=[]
mem=memory(2,10000,10000,50,10,0,0,0,"You are good",0,0,"OFF",0,0)


def initialize_grids(grids):
    c=game_engine.Col()
    t=game_engine.Tile(c)
    grids.append(game_engine.Grid(29,45,position=[15,55],colors=[t.sea[1],t.empty[1],t.land[1],t.house[1],t.woodcutter[1],t.poseidon[1],t.fire[1],c.white,t.forest[1],t.mordor[1],t.mountain[1],t.darklord[1],t.farm[1],t.field[1],t.beach[1],t.townhall[1],t.druidtemple[1]]))
   # terrains=[1]
    grids[0].empty_map()
    grids.append(game_engine.Grid(6,1,position=[1185,380],cell_size=[200,25],margin=5,colors=[c.grey,c.green]))
    grids.append(game_engine.Grid(10,1,position=[1185,50],cell_size=[200,25],margin=5,colors=[c.grey,c.green]))   
    grids.append(game_engine.Grid(10,1,position=[975,50],cell_size=[200,25],margin=5,colors=[c.white]))
    grids.append(game_engine.Grid(3,1,position=[1185,590],cell_size=[200,25],margin=5,colors=[c.grey]))
    grids.append(game_engine.Grid(1,1,position=[975,590],cell_size=[200,85],margin=5,colors=[c.white]))
    grids.append(game_engine.Grid(1,1,position=[975,470],cell_size=[200,85],margin=5,colors=[c.lightgrey]))
    return(grids)

def initialize_ctverce(ctverce,grids):
    ctverce.append([grids[0].margin + grids[0].position[0],
                    grids[0].margin + grids[0].position[1],
                    grids[0].cell_size[0],
                    grids[0].cell_size[1],
                    (255,0,0),
                        2]) 
    ctverce.append([grids[1].margin + grids[1].position[0],
                    grids[1].margin + grids[1].position[1],
                    grids[1].cell_size[0],
                    grids[1].cell_size[1],
                    (255,0,0),
                        2])
    ctverce.append([grids[2].margin + grids[2].position[0],
                    grids[2].margin + grids[2].position[1],
                    grids[2].cell_size[0],
                    grids[2].cell_size[1],
                    (255,0,0),
                        2])
                        
    return(ctverce)

def initialize_labels(labels):
    menu1=["Nothing", "Gather Resources", "Build a house (200)","Build a woodcutter (500)", "Build a farm (300)", "Build a townhall",
           "Build a Druid Temple", "", "", ""]
    for i in range(len(menu1)):    
        labels.append(game_engine.Label([1200,57+30*i],menu1[i],fontsize=15))
        
    menu2=["Reset","Generate Terrain","Smooth Terrain","Plant Trees","Place Poseidon", "Place Dark Lord", "", "Coordinates: ", "Tile type: ", "Game is: "]
    for i in range(len(menu2)):    
        labels.append(game_engine.Label([1200,387+30*i],menu2[i],fontsize=15))
 
    menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Time: "+str(mem.time),"Inhabitants: "+str(mem.inh-mem.used_inh)+"/"+str(mem.inh), "Life: "+str(mem.life), "", "", "", ""]    
    for i in range(len(menu3)):    
        labels.append(game_engine.Label([990,57+30*i],menu3[i],fontsize=15)) #620
        
    headlabelmenu1=["GENERATE WORLD:"]
    labels.append(game_engine.Label([1200,365],headlabelmenu1[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu2=["ACTIONS:"]
    labels.append(game_engine.Label([1200,35],headlabelmenu2[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu3=["GAME VARIABLES:"]
    labels.append(game_engine.Label([990,35],headlabelmenu3[0],color=(255,255,255),fontsize=15))
    
    headlabelmenu4=["TILE INFO:"]
    labels.append(game_engine.Label([1200,575],headlabelmenu4[0],color=(255,255,255),fontsize=15))
    
    headlabelmap=["MAP:"]
    labels.append(game_engine.Label([30,35],headlabelmap[0],color=(255,255,255),fontsize=15))
    
    headlabelalert=["ALERT:"]
    labels.append(game_engine.Label([990,575],headlabelalert[0],color=(255,255,255),fontsize=15))
    
    alertlabel=["You are good"]
    labels.append(game_engine.Label([990,597],alertlabel[0],color=(0,0,0),fontsize=15))
    alertcounter=[""]
    labels.append(game_engine.Label([1160,657],alertcounter[0],color=(0,0,0),fontsize=15))
    gameonstatus=["OFF"]
    labels.append(game_engine.Label([1265,657],gameonstatus[0],color=(0,0,0),fontsize=15))
    gameonlabel=["START/PAUSE"]
    labels.append(game_engine.Label([1002,503],gameonlabel[0],color=(0,0,0),fontsize=25))               
    return(labels)

def evaluate_click(grids,click,t,ctverce):
    map_grids=[grids[0]]
    menu_grids=[grids[1],grids[2]]
    gameon_button=[grids[6]]
    tlist=[t.empty, t.sea, t.land, t.house, t.woodcutter,t.fire, t.mountain, t.forest, t.poseidon, t.mordor, t.darklord, t.farm, t.field, t.beach, t.townhall, t.druidtemple]
    tlist_value=[item[2] for item in tlist]
    for grid in map_grids:
        row,column=grid.evaluate_row_column_indices(click)
        set_element_value(grid,row,column,mem.value,"Player")  
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
        
        if row<=grid.rows and row>=0 and column<=grid.columns and column>=0:    
            ctverce[0][0]=(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0]
            ctverce[0][1]=(grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1]
            ctverce[0][2]=grid.cell_size[0]
            ctverce[0][3]=grid.cell_size[1]
        
    for grid in menu_grids:

        row,column=grid.evaluate_row_column_indices(click)
        
        index=grid.get_element_index(row,column)
        if index is not None:
            if grid==grids[2]:
                function_array=[set_value,set_value,set_value,set_value,set_value,set_value,set_value]
                parameter_array=[0,0,3,4,12,15,16]
                i=2
            elif grid==grids[1]:
                function_array=[reset,generate_terrain,smooth_terrain,plant_trees,place_poseidon,place_darklord,nothing,nothing,nothing]
                parameter_array=[grids[0],grids[0],grids[0],grids[0],grids[0],grids[0],20]
                i=1
                
            if row<=grid.rows and row>=0 and column<=grid.columns and column>=0:
                ctverce[i][0]=(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0]
                ctverce[i][1]=(grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1]
                ctverce[i][2]=grid.cell_size[0]
                ctverce[i][3]=grid.cell_size[1]
            
            function_array[index](parameter_array[index])
        
            print(row, column)
    for grid in gameon_button:
        row,column=grid.evaluate_row_column_indices(click)
        index=grid.get_element_index(row,column)
        if index is not None:
            c=game_engine.Col()
            grids[6].colors=[c.darkgrey]
            mem.gameonbuttoncounter=1
            if mem.gameon !=1:
                mem.gameon=1
            else:
                mem.gameon=0

def nothing(x):
    pass

def reset(grid):
        mem.food=500
        mem.gold=10000
        mem.wood=10000
        mem.time=0
        mem.life=0
        mem.inh=10
        mem.used_inh=0
        mem.value=3
        terrains=[1]
        grid.generate_random_map(terrains)
        mem.gameon=0
        mem.busy_buildings1=[] #cottage
        mem.busy_buildings2=[] #woodcutter
        mem.busy_buildings3=[] #poseidon
        mem.busy_buildings4=[] #farm
        mem.busy_buildings5=[] #townhall
        mem.busy_buildings6=[] #druidtemple
        mem.busy_natureevent1=[] #fires
        
    
    
def generate_terrain(grid):
    terrains=[0,0,0,0,0,0,0,0,2,2,2,2,2]
    grid.generate_random_map(terrains)
    
def plant_trees(grid):
    terrains=[8,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    grid.generate_random_map(terrains,2)
    #if self.grid[i][j]==conditionterrain:
        
# def movement(grid,):
    # grid.grid[row][column] = value
    
def place_poseidon(grid):
    grid.place_randomly(5,0)
    mem.busy_buildings2.append(0) #busy poseidons
    
def place_darklord(grid):
    grid.place_randomly(11,2)
    mem.busy_buildings3.append(0) #busy darklords
    
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
    if value==3 and mem.wood>=200 and mem.inh-mem.used_inh>=0:#house
        return(True)
    elif value==4 and mem.wood>=500 and mem.inh-mem.used_inh>=0:#farm
        return(True)
    elif value==5 and mem.wood>=1000 and mem.inh-mem.used_inh>=0:#poseidon
        return(True)
    elif value==11 and mem.wood>=1000 and mem.inh-mem.used_inh>=0:#darklord
        return(True)
    elif value==12 and mem.wood>=300 and mem.inh-mem.used_inh>=0:#farm
        return(True)
    elif value==15 and mem.wood>=5000 and mem.inh-mem.used_inh>=0:#townhall
        return(True)
    elif value==16 and mem.wood>=5000 and mem.inh-mem.used_inh>=0:#townhall
        return(True)
    
    elif value==6 or value==9 or value==10 or value==13 or value==14 or value==7:
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
    elif value==12:
        mem.wood-=300
        mem.used_inh+=0
    elif value==15:
        mem.wood-=5000
        mem.used_inh+=0
    elif value==16:
        mem.wood-=5000
        mem.used_inh+=0

    
def set_element_value(grid,row,column,value,clicked):
    if not(column>=grid.columns or row>=grid.rows or column<0 or row<0):
        if grid.grid[row][column] in [2]: #0,1,3,4,5,6,8,9,10,11,12,15]: #stavění
            enough_resources=check_resources(value)
            if enough_resources:
                pay_resources(value)
                grid.grid[row][column] = value
                if value==4:
                    mem.busy_buildings1.append(0) #busy woodcutters
                if value==5:
                    mem.busy_buildings2.append(0) #busy poseidons
                if value==11:
                    mem.busy_buildings3.append(0) #busy darklords
                if value==12:
                    mem.busy_buildings4.append(0)  #busy farms
                if value==15:
                    mem.busy_buildings5.append(0)  #busy townhalls
                if value==16:
                    mem.busy_buildings6.append(0)  #busy druidtemples
            else:
                mem.alert="Not enough resources"
                mem.alertcounter=5
                    
        if clicked=="Druid Temple": #kdo kliká
            grid.grid[row][column] = value
        if clicked=="Poseidon": #kdo kliká
            grid.grid[row][column] = value
        if clicked=="Dark Lord": #kdo kliká
            grid.grid[row][column] = value
            print("I will burn all the land!!!!!")
            if value==6:
                mem.busy_natureevent1.append(0) #ohen odpočet
                mem.listoffire_pos.append([row,column])
                print("listoffire",mem.listoffire_pos)
        if clicked=="Fire": #kdo kliká
            print("Ted se meni Fire na Mordor.", mem.busy_natureevent1)
            mem.burnedforests+=1
            grid.grid[row][column] = 9
        if clicked=="Farmer": #kdo kliká
            grid.grid[row][column] = 13
        if clicked=="Woodcutter":
            resource=grid.grid[row][column]
            grid.grid[row][column] = value
            if resource==8:
                mem.wood+=10
                
        if grid.grid[row][column] in [13,8] and clicked=="Player": #klikání obecné. 
            resource=grid.grid[row][column]
            grid.grid[row][column] = 2
            if resource==13:
                mem.food+=10
            if resource==8:
                mem.wood+=10

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
    building2=occurence[5]
    building3 = occurence[9]
    building4 = occurence[12]
    building5 = occurence[15]
    building6 = occurence[16]
    """increment"""
    mem.gold+=houses
    mem.life-=building3
   ## if mem.gold>=4*building2+2*woodcutters:
   ##     mem.gold-=4*building2
   ##     mem.gold-=2*woodcutters
        #mem.food+=farms
        #mem.wood+=woodcutters

   
def time_event(grids,time_fr):
    if mem.gameon==0:
        mem.gameonstatus="OFF"
    else:
        mem.gameonstatus="ON"
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
           # print(mem.busy_buildings1)
            
            buildings_pos=find_buildings(grid,4) # drevorubec kácí
            near_distances,near_positions,near_tile_values=find_nearest_resource(grid,[8],buildings_pos,1000,1000)
            print(near_distances,near_positions,mem.busy_buildings1)
            for i in range(len(mem.busy_buildings1)):
                if mem.busy_buildings1[i]==0:
                    mem.busy_buildings1[i]=5+math.floor(near_distances[i])
                elif mem.busy_buildings1[i]==1:
                    set_element_value(grid,near_positions[i].x,near_positions[i].y,2, "Woodcutter")
                    mem.busy_buildings1[i]-=1
                else:
                    mem.busy_buildings1[i]-=1
            print("busy woodcutters ",mem.busy_buildings1)
            
            buildings_pos=find_buildings(grid,16) # druidtemple seje travicku
            near_distances,near_positions,near_tile_values=find_nearest_resource(grid,[9],buildings_pos,1000,1000)
            print("druidtemple ",near_distances,near_positions,mem.busy_buildings6)
            for i in range(len(mem.busy_buildings6)):
                if mem.busy_buildings6[i]==0:
                    mem.busy_buildings6[i]=3+math.floor(near_distances[i])
                elif mem.busy_buildings6[i]==1:
                    set_element_value(grid,near_positions[i].x,near_positions[i].y,2, "Druid Temple")
                    mem.busy_buildings6[i]-=1
                else:
                    mem.busy_buildings6[i]-=1
            print("busy druidtemple ",mem.busy_buildings6)
            
            
            
            buildings_pos=find_buildings(grid,5) #poseidon dela plaze (grid,tile_value,positions,nexttile_value,building_value)
            near_distances,near_positions,near_tile_values=find_nearest_resource(grid,[2],buildings_pos,0,5) #cislo znaci kterej land hledam
            print(near_distances,near_positions,mem.busy_buildings2)
            for i in range(len(mem.busy_buildings2)):
                 if mem.busy_buildings2[i]==0:
                     mem.busy_buildings2[i]=5+math.floor(near_distances[i])
                 elif mem.busy_buildings2[i]==1:
                    set_element_value(grid,near_positions[i].x,near_positions[i].y,14, "Poseidon") #posledni znaci na co se to zmeni
                    mem.busy_buildings2[i]-=1
                 else:
                     mem.busy_buildings2[i]-=1
            print(mem.busy_buildings2) #odpočet kolik času zbyva do dalsiho zmizeni
            
            
            buildings_pos=find_buildings(grid,11) #mordor tmaví nebo zapaluje
            potentialterrains=[2,3,4,8,12,14,15,16] #cislo znaci kterej land hledam,
            near_distances,near_positions,near_tile_values=find_nearest_resource(grid,potentialterrains,buildings_pos,9,11) # posledni dve omezuji vedle ceho to musi byt
            print("darklord hleda nov mordor", near_distances,near_positions,mem.busy_buildings3)
            for i in range(len(mem.busy_buildings3)):
                if mem.busy_buildings3[i]==0:
                    mem.busy_buildings3[i]=2+math.floor(near_distances[i])#cas co potrebuje mezi konvertovanim kazdeho pole
                elif mem.busy_buildings3[i]==1:
                    print("neartilevalue:",near_tile_values[i])
                    if True in[near_tile_values[i] == zz for zz in [2,14]]: #meni travu na mordor
                          set_element_value(grid,near_positions[i].x,near_positions[i].y,9, "Dark Lord") #posledni znaci na co se to zmeni
                    if any(near_tile_values[i] == zz for zz in [3,4,8,12,15,16]): #meni cokoliv na ohen
                          set_element_value(grid,near_positions[i].x,near_positions[i].y,6, "Dark Lord") #posledni znaci na co se to zmeni
                    mem.busy_buildings3[i]-=1
                else:
                    mem.busy_buildings3[i]-=1
            print(mem.busy_buildings3)
            
            #mem.listoffire_pos
            buildings_pos=find_buildings(grid,6) #ohen se promeni po odpoctu na mordor  #######################
            for i in range(mem.burnedforests,len(mem.busy_natureevent1)):
                 if mem.busy_natureevent1[i]!=50:
                     mem.busy_natureevent1[i]+=1 ###########################
                 else:
                     print("Les ke shoreni je na souradnicich",mem.listoffire_pos[mem.burnedforests])
                     print("Les ke shoreni je na souradnicich",buildings_pos[0].y)     
                     set_element_value(grid,mem.listoffire_pos[mem.burnedforests][0],mem.listoffire_pos[mem.burnedforests][1],9, "Fire") #posledni znaci na co se to zmeni
                   # mem.busy_natureevent1[i]-=1

            print("Fire: ",mem.busy_natureevent1) #odpočet kolik času zbyva do dalsiho zmizeni           
            
    #          terrains=[8,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    # grid.generate_random_map(terrains,2)
    #if self.grid[i][j]==conditionterrain:
            
            
            
            buildings_pos=find_buildings(grid,12) #farma seje fields
            near_distances,near_positions,near_tile_values=find_nearest_resource(grid,[2],buildings_pos,13,12) #cislo znaci kterej land hledam
            print("farma",near_distances,near_positions,mem.busy_buildings4)
            for i in range(len(mem.busy_buildings4)):
                if mem.busy_buildings4[i]==0:
                    mem.busy_buildings4[i]=15+math.floor(near_distances[i])
                elif mem.busy_buildings4[i]==1:
                    if near_distances[i]<=1.5: # timto omezuji pusobeni farmy
                        set_element_value(grid,near_positions[i].x,near_positions[i].y,13, "Farmer") #posledni znaci na co se to zmeni
                    mem.busy_buildings4[i]-=1
                else:
                    mem.busy_buildings4[i]-=1
            print(mem.busy_buildings4)
            
        
def find_buildings(grid,tile_value):
    buildings_pos=[]
    for row in range(grid.rows):
        for column in range(grid.columns):
            if grid.grid[row][column]==tile_value:
                buildings_pos.append(game_engine.Position([row,column]))
                
                
    return(buildings_pos)
    

def find_nearest_resource(grid,tile_value,positions,nexttile_value,building_value):
 
    #if any(t < 0 for t in x):
    # do something   
    near_distances=list(range(100,100+len(positions)))
    near_positions=list(range(100,100+len(positions)))
    near_tile_values=list(range(100,100+len(positions)))
    for row in range(grid.rows):
        for column in range(grid.columns):
            if any(grid.grid[row][column]==z for z in tile_value):
                if nexttile_value != 1000: #a zaroven by se dalo rict ze building_value musi byt 1000 ale nastava to ve stejnych pripadech
                    if (grid.grid[row-1][column]==nexttile_value or grid.grid[row-1][column]==building_value or grid.grid[row+1][column]==nexttile_value or grid.grid[row+1][column]==building_value or grid.grid[row][column-1]==nexttile_value or grid.grid[row][column-1]==building_value or grid.grid[row][column+1]==nexttile_value or grid.grid[row][column+1]==building_value): #or grid.grid[row+1][column]==(nexttile_value or building_value) or grid.grid[row][column-1]==(nexttile_value or building_value) or grid.grid[row][column+1]==(nexttile_value or building_value):   
                        pos=game_engine.Position([row,column])
                        for i in range(len(positions)):
                            dist=pos.distance(positions[i])
                            if dist<near_distances[i]:
                                near_distances[i]=dist
                                near_positions[i]=pos
                                near_tile_values[i]=grid.grid[row][column]
                else:    
                    pos=game_engine.Position([row,column])
                    for i in range(len(positions)):
                        dist=pos.distance(positions[i])
                        if dist<near_distances[i]:
                            near_distances[i]=dist
                            near_positions[i]=pos
                            near_tile_values[i]=grid.grid[row][column]
                            #if dist>99:#fixnuti toho ze se zasekne dark lord kdyz pali lesy a nema kam jit
                            #    dist=3
    print(near_distances,near_positions,near_tile_values)
    return(near_distances,near_positions,near_tile_values)
                    

    


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
    c=game_engine.Col()
    labels[20].text="Gold: "+str(round(mem.gold))
    labels[21].text="Wood: "+str(round(mem.wood))
    labels[22].text="Food: "+str(round(mem.food))
    labels[23].text="Time: "+str(round(mem.time))
    labels[24].text="Life: "+str(round(mem.life))
    labels[25].text="Inhabitants: "+str(round(mem.inh-mem.used_inh))+"/"+str(round(mem.inh))
    labels[17].text="Coordinates: "+str(mem.row)+","+str(mem.column)
    labels[18].text="Tile type: "+str(mem.tiletypename)
    labels[38].text=mem.gameonstatus
    if mem.gameon == 1:
        labels[38].color=c.green
    else:
        labels[38].color=c.red

def update_alerts(labels,grids):
    c=game_engine.Col()
    if mem.alertcounter>=0:
        #labels[37].text=str(mem.alertcounter)
        mem.alertcounter-=1
        grids[5].colors=[c.red]
    else:
        mem.alert = "You are good"
        grids[5].colors=[c.white]
    labels[36].text=mem.alert
    
    if mem.gameonbuttoncounter>=0:
        #labels[37].text=str(mem.alertcounter)
        mem.gameonbuttoncounter-=1
    else:
        grids[6].colors=[c.lightgrey]
        
    labels[36].text=mem.alert
    
    
    
    
        


        #menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Inhabitants: "+str(mem.inhabitants)]    
    #for i in range(len(menu3)):    
     #   labels.append(game_engine.Label([1020,70+55*i],menu3[i],fontsize=20))