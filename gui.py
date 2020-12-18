from tkinter import filedialog
from tkinter import *


def getFile():
    root.fileName = filedialog.askopenfilename(filetypes=[("LOL File", "*.lol")], initialdir="tests/",title = "Select a LOL Code File")     # Get the LOL File 


root = Tk()
root.title("League of LolCode")         # Title
root.iconbitmap("favicon.ico")          # Icon


fileButton = Button(root, text="Select File",command = getFile,borderwidth = 3,bg ="SlateGray1")     # Button Used for Getting a LOL Fil
execButton = Button(root, text="Execute")

topMainFrame = LabelFrame(root,text="Top Main Frame",bg="cyan2") 
codeFrame = LabelFrame(topMainFrame,text="Code Editor",padx=200,bg = "yellow") 
lexFrame = LabelFrame(topMainFrame,text="Lexemes",padx=200,bg = "red") 
symbolFrame = LabelFrame(topMainFrame,text="Symbol Table",padx=200,bg = "blue") 

bottomMainFrame = LabelFrame(root,text="Bottom Main Frame",bg="orange")  
buttonFrame = LabelFrame(bottomMainFrame,text="Buttons",padx=200,bg = "purple") 
outFrame = LabelFrame(bottomMainFrame,text="Output",padx=200,bg = "green") 


test1 = Label(codeFrame,text="test 1")
test2 = Label(lexFrame,text="test 2")
test3 = Label(symbolFrame,text="test 3")

test4 = Label(buttonFrame,text="test 4")
test5 = Label(outFrame,text="test 5")


test1.pack()
test2.pack()
test3.pack()
test4.pack()
test5.pack()

topMainFrame.grid_columnconfigure(0,weight=1)   # Balance the columnd width on each window
topMainFrame.grid_columnconfigure(1,weight=1)
topMainFrame.grid_columnconfigure(2,weight=1)

topMainFrame.pack(fill="both",expand=True)
codeFrame.grid(row=0,column=0)
lexFrame.grid(row=0,column=1)
symbolFrame.grid(row=0,column=2)

bottomMainFrame.pack(fill="both",expand=True)
buttonFrame.grid(row=0,column=0)
outFrame.grid(row=0,column=1,columnspan=3)




root.mainloop() 