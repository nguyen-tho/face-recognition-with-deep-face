
import tkinter as tk
from tkinter import messagebox,PhotoImage
from tkinter import font as tkfont
import create_dataset as data
import verify_user as v
import verify_users as v2

data.get_nameslist()
names = data.read_nameslist()
class mainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Simple Attendance System")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()
            
    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()
        
        
class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   Sign up  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Face Recognition  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageSix"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Submit", fg="#ffffff", bg="#263942", command=self.submit)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
    def submit(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        self.controller.active_name = name
        self.controller.frames["PageTwo"]
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Enter your username", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        #self.menuvar = tk.StringVar(self)
        #self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        #self.dropdown.config(bg="lightgrey")
        #self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg="#263942")
        #self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
        
    def next_foo(self):
        if self.user_name.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.user_name.get()
        self.controller.show_frame("PageFive")  
        
    def clear(self):
        self.user_name.delete(0, 'end')
    '''
    def refresh_names(self):
        global names
        self.user_name.
        #self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.user_name, name))
    '''

'''
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")
'''

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Confirm", fg="#ffffff", bg="#263942",command=self.confirm)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = data.create_dataset(self.controller.active_name)
        self.controller.num_of_images = data.number_of_samples(self.controller.active_name)
        self.numimglabel.config(text=str(f"Number of images captured = {data.number_of_samples(self.controller.active_name)}"))
        data.get_nameslist()

    def confirm(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 100 images!")
            return
        else:
            v.update_pkl_file(self.controller.active_name)# update pkl file for a first time
           
        '''
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        '''
        self.controller.show_frame("PageSix")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Find identity Features", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Find identity on an image", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button2 = tk.Button(self, text="Find identity Realtime (1 person)", command=self.find, fg="#ffffff", bg="#263942")
        button3 = tk.Button(self, text="Find identity Realtime (more than 1 person)", command=self.findPeople, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        v.check_attendance_v2()
        self.controller.show_frame("StartPage")
        
    def find(self):
        v.find_identity()
        #self.controller.show_frame("StartPage")
        
    def findPeople():
        v2.check_users()
        
    '''
    def gender_age_pred(self):
       ageAndgender()
    def emot(self):
        emotion()
'''

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Verify user Features", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Verify on an image", command=self.verify_image, fg="#ffffff", bg="#263942")
        button2 = tk.Button(self, text="Verify Realtime", command=self.verify_realtime, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
               
    def verify_realtime(self):
        v.check_realtime(self.controller.active_name)
    def verify_image(self):
        v.check_attendance(self.controller.active_name)

class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Features", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Verify user", command=lambda: self.controller.show_frame("PageTwo"), fg="#ffffff", bg="#263942")
        button2 = tk.Button(self, text="Find user", command=lambda: self.controller.show_frame("PageFour"), fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
app = mainUI()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()

