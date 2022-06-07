import tkinter as tk
from manual_control import Manual
from auto_control import Auto
class Manual_Auto:
    def __init__(self,istrue):
        #TKinter
        self.root = tk.Tk()
        self.root.geometry("200x150")
        
        self.istrue = istrue
        
        if self.istrue == True:
            self.istrue = True
        else:
            self.root.destroy()
        
        self.manual_button = tk.Button(self.root,text = 'Manual',font = ('Calibri',15,'bold'), bg = '#FD7D00', width = 15,command = self.manual_window)
        self.manual_button.grid(row = 0, column = 0, padx = 10, pady = 20)
        
        self.auto_button = tk.Button(self.root, text = 'Automatic', font = ('Calibri',15,'bold'), bg = '#FD7D00', width = 15,command = self.automatic_window)
        self.auto_button.grid(row = 1, column = 0, padx = 10, pady = 20)
    
    def manual_window(self):
        self.root.destroy()
        m = Manual()
        m.manual_camera()

    def automatic_window(self):
        self.root.destroy()
        a = Auto()
        a.Auto_camera()

if __name__ == "__main__":
    ma = Manual_Auto(False)