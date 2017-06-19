from constellations import *
from Tkinter import *
import random
import tkMessageBox
import time
from time import sleep
#import pygame


global count
global x_input
global y_input
                          
count = 1
x_input = 1
y_input= 0    


#pygame.init()


#winSound = pygame.mixer.Sound("applause.wav")
#loseSound = pygame.mixer.Sound("explosion.wav")




class Skysweeper():

    def __init__(self, master):
        #create frame window
        global window
        window = Frame(height = 32, width = 32, bg = "black", padx = 10, pady = 10)
        window.pack()

        #images being used in GUI 
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/my_sky.gif")
        self.tile_mine = PhotoImage(file = "images/gold_star.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
        self.title = PhotoImage(file = "images/title.gif")
  

        #gives tiles numbers representing mine proximity
        self.tile_num = []
        for x in range(1, 9):
            self.tile_num.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        #variables for win conditions
        self.flags = 0
        self.correct = 0
        self.clicked = 0
        #variables for button and mine placement 
        self.mines = 0
        self.tiles = {}
        
        #labels for GUI aesthetics  
        #self.label5 = Label(window, text = "Time: "+str(start_time))
        self.label4 = Label(window, text = "Level: "+str(count))
        self.label3 = Label(window, text = "Flags: "+str(self.flags))
        self.label2 = Label(window, text = "Mines: "+str(self.mines))
        self.label_title = Label(window, image = self.title)

        pick()

        #where logic for grid layout begins
        self.grid_1(144)

        #lay buttons in grid
        for x in self.tiles:
            self.tiles[x][0].grid( row = self.tiles[x][4][0], column = self.tiles[x][4][1] )

        
        #button for resetting game
        b = Button(window, text = "Reset", command = self.reset,fg = "white", bg = "black", font =("Calibri", 10))
        b.grid(row = 16, column = 10, columnspan = 5, sticky = E)
        self.nearbyMines()
        #self.cheat()

    ###end of init####
  
    def reset(self):
        message3 = tkMessageBox.askyesno(title= "Reset?" , message= "Are you sure you want to reset? You will restart at level 1." )
        if message3 == True:
            global count
            count = 1
            self.label4.config(text = "Level: "+str(count), width = 10)
            sys.exit
            game.destroy()
            main()
        else:
            pass
                     
    def grid_1(self,value):
        x_input = 1
        y_input = 0
        global mine
        self.label_title.grid(row = 0, column = 0, columnspan = 12) 
        #loop that creates grid based upon size of range
        for x in range (value):
                mine = 0
                default_img = self.tile_plain
                #lazy
                #constellation placement
                if picked == "Libra":
                    if Libra(x_input,y_input):
                        mine = 1
                        self.mines += 1
                if picked == "Cancer":
                    if Cancer(x_input,y_input):
                        mine = 1
                        self.mines += 1
                if picked == "Leo":
                    if Leo(x_input,y_input):
                        mine = 1
                        self.mines += 1
                if picked == "Capricorn":
                    if Capricorn(x_input,y_input):
                        mine = 1
                        self.mines += 1 
                if picked == "Virgo":
                    if Virgo(x_input,y_input):
                        mine = 1
                        self.mines += 1   
                if picked == "Aquarius":
                    if Aquarius(x_input,y_input):
                        mine = 1
                        self.mines += 1 
                if picked == "Scorpio":
                    if Scorpio(x_input,y_input):
                        mine = 1
                        self.mines += 1       

                    #Keys:
                    #0 button widget
                    #1 mine (1 = yes , 0 = no)
                    #2 state 0 = unclicked, 1 = clicked, 2 = flagged)
                    #3 button x value
                    #4 [x, y] coordinates
                    #5 nearby mines
                # instantiate button, x [x] is called from the previously set dictionary
                self.tiles[x] = [Button(window, image = default_img),mine,0,x,[x_input, y_input], 0]
                self.tiles[x][0].bind('<Button-1>',self.leftClick_wrapper(x))
                self.tiles[x][0].bind('<Button-3>',self.rightClick_wrapper(x))


                # calculate coords:
                y_input += 1
                if y_input == 12:
                    y_input = 0
                    x_input += 1
               

        #bottom of GUI (mines, flags, level)
        #number of mines displayed
        self.label2.config(text = "Mines: "+str(self.mines), width = 10, font =("Calibri", 18,"bold"),fg = "white",bg = "black")
        self.label2.grid(row = 20, column = 0, columnspan = 4,rowspan = 4, sticky = W)
                         
        #number of flags displayed
        self.label3.config(text = "Flags: "+str(self.flags), width = 10, font =("Calibri", 18,"bold"),fg = "white",bg = "black")
        self.label3.grid(row = 20, column = 4, columnspan = 4,rowspan = 4, sticky = "")
        
        #level displayed
        self.label4.config(text = "Level: "+str(count),width = 10, font =("Calibri", 18,"bold"),fg = "white",bg = "black")
        self.label4.grid(row = 20, column = 8, columnspan = 4,rowspan = 4, sticky = E)
        
        #self.label5.config(text = "Time: "+str(start_time), width = 10, font =("Calibri", 18,"bold"),fg = "white",bg = "black")
        #self.label5.grid(row = 20, column = 6, columnspan = 2,rowspan = 4, sticky = E)
        

    def rightClick_wrapper(self, x):
        return lambda Btn: self.rightClick(self.tiles[x])

    def leftClick_wrapper(self, x):
        return lambda Btn: self.leftClick(self.tiles[x])

    #if left clicked
    def leftClick(self, btn):
        if btn[1] == 1: #if a mine
            # show all mines and check for flags
            for x in self.tiles:
                if self.tiles[x][1] != 1 and self.tiles[x][2] == 2:
                    self.tiles[x][0].config(image = self.tile_wrong)
                if self.tiles[x][1] == 1 and self.tiles[x][2] != 2:
                    self.tiles[x][0].config(image = self.tile_mine)
            # end game
            self.loseGame()
        else:
            #change image
            if btn[5] == 0:
                btn[0].config(image = self.tile_clicked)
                self.clearTiles(btn[3])
            else:
                btn[0].config(image = self.tile_num[btn[5]-1])

            # if not already set as clicked, change state and count
            if btn[2] != 1:
                btn[2] = 1
                self.clicked += 1
        self.check_win()

    #if right clicked       
    def rightClick(self, btn):
        print btn[3], btn[4]
        # if not clicked
        if btn[2] == 0:
            btn[0].config(image = self.tile_flag)
            btn[2] = 2
            btn[0].unbind('<Button-1>') 
            # if a mine
            if btn[1] == 1:
                self.correct += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif btn[2] == 2:
            btn[0].config(image = self.tile_plain)
            btn[2] = 0
            btn[0].bind('<Button-1>', self.leftClick_wrapper(btn[3]))
            # if a mine
            if btn[1] == 1:
                self.correct -= 1
            self.flags -= 1
            self.update_flags()
        self.check_win()
       
            
    
    def update_flags(self):
        self.label3.config(text = "Flags: " +str(self.flags))
        print self.flags

    #check tile[x] for mines 
    def check_mines(self, x):
        try:
            if self.tiles[x][1] == 1:
                return True
        except KeyError:
            pass

    #checks each button for mines near it and totals it in the nearbymines variable
    #+13 +12 +11    
    #+1   x  -1
    #-11 -12 -13
    #visual representation of checking     
    def nearbyMines(self):     
            for x in self.tiles:
                nearbymines = 0
                check_area = self.tiles[x][3]
                check_area = [(x+13),(x+12),(x+11),(x+1),(x-1),(x-11),(x-12),(x-13)]
                for i in range(len(check_area)):
                    if self.check_mines(check_area[i]):
                        nearbymines += 1
                #update each tile with amount of mines near it
                self.tiles[x][5] = nearbymines
      
    #takes x value from self.tiles
    def checkTile(self,x, keys):
        try:     
            if self.tiles[x][2] == 0:
                if self.tiles[x][5] == 0 and self.tiles[x][1] == 0:
                    self.tiles[x][0].config(image = self.tile_clicked)
                    keys.append(x)
                else:
                    self.tiles[x][0].config(image = self.tile_num[self.tiles[x][5]-1])
                self.clicked += 1
                self.tiles[x][2] = 1
        except KeyError:
            pass
    #checks nearby tiles during left click reveal event
    def clearTiles(self,x):
        keys = [x]
        for x in keys:
            self.checkTile(x+11, keys)  
            self.checkTile(x+12, keys)     
            self.checkTile(x+13, keys)  
            self.checkTile(x+1, keys)      
            self.checkTile(x-1, keys)      
            self.checkTile(x-13, keys)     
            self.checkTile(x-12, keys)     
            self.checkTile(x-11, keys)  

    def loseGame(self):
        for x in self.tiles:
            if self.tiles[x][2] == 0:
                    if self.tiles[x][5] == 0 and self.tiles[x][1] == 0:
                        self.tiles[x][0].config(image = self.tile_clicked)
                    else:
                        self.tiles[x][0].config(image = self.tile_num[self.tiles[x][5]-1])
            if self.tiles[x][1] == 1:
              self.tiles[x][0].config(image = self.tile_mine)
        message = tkMessageBox.askyesno(title="Game Over!", message = "You have lost. Play again?")
        if message == True:     
            sys.exit
            game.destroy()
            main()  

        elif message == False:
            sys.exit
            game.destroy()
                
              
    def winGame(self):
        self.label4.config(text = "Level: "+str(count), width = 10)
        if len(reg_constellations) != 0:
            del reg_constellations[0]
            #print reg_constellations
        else:
            for x in self.tiles:
                self.clearTiles(self.tiles[x][3])
        window2 = tkMessageBox.askyesno(title= "You Beat Level: "+str(count)+"!", message= "You have beaten "+str(picked)+". Continue?" )
        levelCount()
        if window2 == True:
            sys.exit
            game.destroy()
            main()
        else:
            game.destroy()
        
    def check_win(self):
        if self.correct == self.mines or self.clicked == 144-self.mines: 
            self.winGame()
      
    def cheat(self):
      for x in self.tiles:
          #self.clearTiles(self.tiles[x][3])
          if self.tiles[x][1] == 1:
              self.tiles[x][0].config(image = self.tile_mine)
  
         
def main():
    global game
    #create Tk widget
    game = Tk()
    #set program title
    game.title("Skysweeper")
    #create game instance
    skysweeper = Skysweeper(game)
    game.mainloop()


def levelCount():
     global count
     count += 1   


reg_constellations = ['Leo', 'Libra', 'Cancer',
                      'Capricorn', 'Virgo', 'Scorpio', 'Aquarius' ]

#picks a random constellation
def pick():
    global picked
    picked = 0
    global big_constellations
    big_constellations = {}
    global reg_constellations
    if len(reg_constellations) == 0:
        reg_constellations = ['Leo', 'Libra', 'Cancer',
                              'Capricorn', 'Virgo', 'Scorpio', 'Aquarius' ]    
    #picks constellation randomly from list,
    #then eventually deletes it from the list to prevent repeated levels
    if reg_constellations != 0: 
        random.shuffle(reg_constellations)
        picked = reg_constellations[0]
        #print picked
    #refreshes list of constellations if player makes it this far
    
        

main()


global start_time
start_time = time.clock()
def keep_time():
    watch = int(round(start_time)) 
    Skysweeper.label5.config(text = "Time: "+ (int(round(watch))))
    keep_time()    



  

                                           
                                           
                                           

