from tkinter import ttk
from tkinter import filedialog
from tkinter import *


def getFile():
    root.fileName = filedialog.askopenfilename(filetypes=[("LOL File", "*.lol")], initialdir="tests/",title = "Select a LOL Code File")     # Get the LOL File 

def clearCodeFrame():
    pass

def executeCode():
    pass



root = Tk()                             # root 
root.title("League of LolCode")         # Title
root.iconbitmap("favicon.ico")          # Icon
root.geometry("1700x900")               # Default window size is 1600x900

topMainFrame = LabelFrame(root,bg="gray17") 

codeFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                   # Code Editor Frame
codeScroll = Scrollbar(codeFrame,orient ="vertical")
codeEditor = Text(codeFrame,width=50,height=17,font=("Helvetica",12),background="LightSteelBlue4",selectbackground="DodgerBlue2",selectforeground="black",undo=True,yscrollcommand=codeScroll.set)

symbolFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                # Lexemes Frame 
symbolView = ttk.Treeview(symbolFrame, selectmode="browse",height=18)
symbolView['show'] = 'headings'                                                                     # Remove empty first column
symbolView["columns"] = ("1", "2") 
symbolView.column("1", width = 250, anchor ='center') 
symbolView.column("2", width = 250, anchor ='e') 
symbolView.heading("1", text="Identifier") 
symbolView.heading("2", text="Value") 
symbolScroll = ttk.Scrollbar(symbolFrame,orient ="vertical",command = symbolView.yview)
symbolView.configure(yscrollcommand = symbolScroll.set)

lexFrame = LabelFrame(topMainFrame,relief='flat',borderwidth=3,bg="dodgerblue3")                        # Symbol Table Frame 
lexView = ttk.Treeview(lexFrame, selectmode="browse",height=18)
lexView['show'] = 'headings'                                                                        # Remove empty first column
lexView["columns"] = ("1", "2") 
lexView.column("1", width = 250, anchor ='center') 
lexView.column("2", width = 250, anchor ='e') 
lexView.heading("1", text="Lexeme") 
lexView.heading("2", text="Classification") 
lexScroll = ttk.Scrollbar(lexFrame,orient ="vertical",command = lexView.yview)
lexView.configure(yscrollcommand = lexScroll.set)

bottomMainFrame = LabelFrame(root,bg="gray17")  

buttonFrame = LabelFrame(bottomMainFrame,bg="dodgerblue3",padx=50,pady=10,height=12) 
fileButton = Button(buttonFrame, text="Select File",bd=3,command=getFile, borderwidth = 2,bg ="SlateGray1",width=20,height=3)            # Button Used for Getting a LOL File
execButton = Button(buttonFrame, text="Execute ",bd=3,command=executeCode, borderwidth = 2,bg ="SlateGray1",width=20,height=3)           # Button for executing code in the code frame
clearButton = Button(buttonFrame, text="Clear Editor",bd=3,command=clearCodeFrame ,borderwidth = 2,bg ="SlateGray1",width=20,height=3)   # Button for Clearing the code frame 

outFrame = LabelFrame(bottomMainFrame,bg="dodgerblue3",height=300,borderwidth = 2,) 
outPut = Text(outFrame,width=110,height=16,font=("Helvetica",12,"bold"),background="LightSteelBlue4",selectbackground="DodgerBlue2",selectforeground="black")

codeLabel = Label(codeFrame,text="Code Editor",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")
lexLabel = Label(lexFrame,text="Lexemes",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")
symbolLabel = Label(symbolFrame,text="Symbol Table",font=("Helvetica",15,"bold"),width=30,height=1,bg ="dodgerblue3")

buttonLabel = Label(buttonFrame,text="Buttons",bg ="LightSteelBlue4",font=("Helvetica",15,"bold"),width=20,height=2)

topMainFrame.pack(fill='both',expand=True)                                 # Top Main Frame Arrangement
codeFrame.grid(row=0,column=0,padx=10,pady=5)
lexFrame.grid(row=0,column=1,padx=10,pady=5)
symbolFrame.grid(row=0,column=2,padx=10,pady=5)

codeLabel.pack()
codeScroll.pack(side="right",fill="y")
codeEditor.pack()

lexLabel.pack()                                     # Lex Frame Arrangement
lexScroll.pack(side="right",fill="y")
lexView.pack()

symbolLabel.pack()                               # Symbol Frame Arrangement
symbolScroll.pack(side="right",fill="y")
symbolView.pack()

bottomMainFrame.pack(fill='both',expand=True)                            # Bottom Main Frame Arrangement
buttonFrame.grid_rowconfigure(0,weight=1)
buttonFrame.grid_rowconfigure(1,weight=1)
buttonFrame.grid_rowconfigure(2,weight=1)
buttonFrame.grid(row=0,column=0,padx=5,pady=10)
outFrame.grid(row=0,column=1,columnspan=2,padx=5,pady=10)




outPut.pack(side="left",fill="both",padx=5,pady=5)

buttonLabel.grid(row=0,padx=8,pady=10)                                  # Button Frame Arrangement 
fileButton.grid(row=1,padx=8,pady=10)
execButton.grid(row=2,padx=8,pady=10)
clearButton.grid(row=3,padx=8,pady=10)




root.mainloop() 

