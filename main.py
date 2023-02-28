#!/usr/bin/env python3 

from dashboard import Dashboard
from tkinter import *
root = Tk()
T = Text(root, height=100, width=100)
T.pack()
T.insert(2.0, 'GeeksforGeeks\nBEST WEBSITE\n')
T.insert(3.0, 'GeeksforGeeks\nBEST WEBSITE\n')
T.insert(4.0, 'GeeksforGeeks\nBEST WEBSITE\n')
T.insert(5.0, 'GeeksforGeeks\nBEST WEBSITE\n')
T.insert(1.0, u'GeeksforGeeks\nBEST WEBSITE\u1359')
mainloop()
