from random import *
from tkinter import *
from tkinter import messagebox

root=Tk()
root.resizable(False,False)
#keeps window at top
root.attributes('-topmost', True)

numRow = int(input("How many rows?:\t\t"))
numCol = int(input("How many columns?:\t"))

while (numRow-numCol>5 or numCol-numRow>5) or (numRow>40 or numCol>40):
    print("\nCan't be a difference of more than 5 and must be less than 40 cols / rows")
    numRow = int(input("How many rows?:\t\t"))
    numCol = int(input("How many columns?:\t"))

#creates 2d array for values (9 = mine, 1-8 = mines around)
valTable = [[0 for a in range(numCol)] for b in range(numRow)]
#empty array
btnTable=[]

clickCounter=0
mineCounter=0

# random places for mines
numMine = (numCol*numRow)//6
linearMineLocation=sample(range(numRow*numCol),numMine)

for i in range(numMine):
    valTable[linearMineLocation[i]//numCol][linearMineLocation[i]%numCol] = 9
print(valTable)

def end(msg):
    messagebox.showinfo("End of game", msg)
    root.destroy()
    #quit()

def open0(i,j):
    global clickCounter
    for a in range(-1,2):
        for b in range(-1,2):
            if (i+a >= 0 and j+b >= 0 and i+a < numRow and j+b < numCol) and (str(btnTable[i+a][j+b]['state'])=="normal") and (str(btnTable[i+a][j+b]['text'])!="*"):
                btnTable[i+a][j+b].configure(state="disabled")
                if valTable[i+a][j+b]!=9:
                    btnTable[i+a][j+b].configure(bg=("gray"+str((90-valTable[i+a][j+b]*5))))
                if valTable[i+a][j+b]==0:
                    open0(i+a,j+b)
                else:
                    btnTable[i+a][j+b].config(text=valTable[i+a][j+b])
                clickCounter+=1
    return clickCounter

def check_win(clickCounter,mineCounter):
    if clickCounter == (numCol*numRow)-numMine and numMine==mineCounter:
        msg="WINNER"
        for i in range(numRow):
            for j in range(numCol):
                btnTable[i][j].configure(state="disabled")
        end(msg)

def left_click(event,i,j):
    global mineCounter
    global clickCounter
    
    if valTable[i][j] == 9 and str(btnTable[i][j]["text"])!="*":
        btnTable[i][j].configure(bg="red")
        msg="LOSER"
        end(msg)
        
    elif str(btnTable[i][j]['state'])=="normal":
        btnTable[i][j].configure(state="disabled")
        #only opens 8 surrounding boxes
        btnTable[i][j].configure(bg=("gray"+str((90-valTable[i][j]*5))))
        if valTable[i][j]==0:
            open0(i,j)
        else:
            btnTable[i][j].config(text=valTable[i][j])
        clickCounter+=1        
        check_win(clickCounter,mineCounter)
                        
def middle_click(event,i,j):
    print(j,i)

def right_click(event,i,j):
    global mineCounter
    global clickCounter
    
    if str(btnTable[i][j]['state'])=="normal" and btnTable[i][j]["text"]!="*":
        btnTable[i][j].configure(state="disabled")
        btnTable[i][j].config(text="*")
        mineCounter+=1
    elif btnTable[i][j]["text"]=="*":
        btnTable[i][j].configure(state="normal")
        btnTable[i][j].config(text="")
        mineCounter-=1
    check_win(clickCounter,mineCounter)
    #minesLeft.config(textvariable=mineCounter)

for i in range(numRow):
    btnTableX=[]
    for j in range(numCol):
        if numRow>20:
            btn = Button(root, height=1,width=2)
        else:
            btn = Button(root, height=2,width=4)
        btn.grid(row=i+1,column=j)
        # i=i makes sure the i passed isn't the last value of the loop
        btn.bind('<Button-1>',lambda event, i=i, j=j: left_click(event,i,j))
        btn.bind('<Button-2>',lambda event, i=i, j=j: middle_click(event,i,j))
        btn.bind('<Button-3>',lambda event, i=i, j=j: right_click(event,i,j))
        btnTableX.append(btn)
        
        #changing values dependant on surrounding mines
        #in 2d array, x and y coordinates order are flipped (draw out to understand)

        if valTable[i][j]!=9:
            for a in range(-1,2):
                for b in range(-1,2):
                    #avoids values outside table
                    if i+a >= 0 and j+b >= 0 and i+a < numRow and j+b < numCol:
                        if valTable[i+a][j+b]==9:
                            valTable[i][j]+=1
        
    btnTable.append(btnTableX)

root.mainloop()
