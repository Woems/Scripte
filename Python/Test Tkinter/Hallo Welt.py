#!/usr/bin/python
#Example (Hello, World):
from Tkinter import *
tk = Tk()
tk.title("FritzBox Bandbreitenmonitor")
frame = Frame(tk)
frame.pack(fill="both",expand=1)
label = Label(frame, text="Hallo Welt!")
label.pack(expand=0)
label = Label(frame, text="Hallo Welt2!")
label.pack(expand=0)
button = Button(frame,text="OK",command=tk.destroy)
button.pack(side="bottom")
tk.geometry("400x100+1200+1050")
tk.mainloop()
