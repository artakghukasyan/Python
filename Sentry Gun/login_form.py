import tkinter as tk
from App import App

# Main Function

def main():
    root = tk.Tk()
    app = Login(root)

    # Root configurations
    root.config(bg = '#131313')
    root.resizable(False,False)
    root.mainloop()


#Desktop App

class Login:
    def __init__(self,root):
        #Root settings
        self.root = root
        self.root.geometry("500x400")
        self.root.title("Sentry gun")
        self.root.bind("<Return>", self.login)

        #Login text Frame 
        self.login_frame = tk.Frame(self.root, width = 500, height = 80, bg='#131313')
        self.login_frame.pack(side=  'top')
        self.login_text = tk.Label(self.login_frame, text = "ՄՈՒՏՔ", bg='#131313', fg = '#E9E9E9', font = ("Arial",20,'bold'))
        self.login_text.grid(column= 0, row = 0, pady = 30)

        #Username - Password frame

        self.user_frame = tk.Frame(self.root, width = 500, height= 420, bg= '#131313')
        self.user_frame.pack(pady =10)

        # Username

        self.username_text = tk.Label(self.user_frame, text = 'ԳԱՂՏՆԱՆՈՒՆ', bg= "#131313", fg='#595959',font = ("Calibri",10,'bold'))
        self.username_text.grid(row = 0, column = 0, stick = 'w')
        self.username_entry = tk.Entry(self.user_frame, width = 40, bg= '#202425', justify =tk.CENTER, fg = '#fff',font = ("Calibri", 15,'bold'))
        self.username_entry.grid(pady = 10, ipady = 5, column = 0, row = 1)

        # Password

        self.password_text = tk.Label(self.user_frame, text = 'ԳԱՂՏՆԱԲԱՌ', bg= "#131313", fg='#595959',font = ("Calibri",10,'bold'))
        self.password_text.grid(column = 0, row = 2, stick ='w')
        self.password_entry = tk.Entry(self.user_frame, width = 40, bg= '#202425', fg ='#fff', justify = tk.CENTER,show = '*',font = ("Calibri", 15,'bold'))
        self.password_entry.grid(ipady = 5, pady = 10, column = 0, row  = 3)

        # Errors field

        self.errors_text = tk.Label(self.user_frame,text = '', bg= '#131313')
        self.errors_text.grid(row = 4, column =0,stick = 'w', pady = 5) 

        # Button
        self.button = tk.Button(self.user_frame, text = 'ՄՈՒՏՔ',bg = '#0386FC', fg = '#BDF4FF',width = 15, font = ("Arial", 15,'bold'), command = self.login)
        self.button.grid(row = 5 ,column = 0, pady = 10)

    def login(self, event = None):
        self.username_value = self.username_entry.get()
        self.password_value = self.password_entry.get()

        if self.username_value == 'admin' and self.password_value == 'Kalavan2022':
            self.errors_text.config(text = "Հաջողութամբ մուտք եք գործել", fg = 'green')
            self.username_entry.delete(0,tk.END)
            self.password_entry.delete(0,tk.END)
            self.root.destroy()
            App(True)
        else:
            self.errors_text.config(text="գաղտնանունը կամ գաղտնաբառը սխալ են մուտքագրված",fg= 'red')
            self.username_entry.delete(0,tk.END)
            self.password_entry.delete(0,tk.END)



if __name__ == '__main__':
    main()

