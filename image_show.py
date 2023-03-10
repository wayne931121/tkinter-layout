import os, time, threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
root = tk.Tk()
root.title("Example"); scale=1.8;
root.geometry("{}x{}+450+300".format(int(360*scale), int(200*scale)))



def chooseFolder():
    directory = filedialog.askdirectory()
    if directory=="": return
    label_folder_explorer.config(text=directory)
    return directory

def OK():
    global ImageManager
    folder = label_folder_explorer["text"]
    if folder=="Choose Folder":
        return None
    files = os.listdir(folder)
    images = []
    for i in files:
        if i.split(".")[-1]=="jpg" or i.split(".")[-1]=="png":
            images.append(os.path.join(folder, i).replace("\\","/"))
    ImageManager = Image_Manager(canvas, label_image_name, images)
    button_left.config(command=lambda:ImageManager.switch_image("left"))
    button_right.config(command=lambda:ImageManager.switch_image("right"))
    page2.tkraise()

class Image_Manager():
    def __init__(self, canvas, label_name, images):
        self.canvas = canvas #place image
        self.label_name = label_name
        self.images = images
        self.cache = [self.load_image(-1), self.load_image(0), self.load_image(1)]
        self.onConfigure = False
        self.state = ""
        #self.relative_resize_image(self.cache, self.canvas, self.label_name)
        self.canvas.bind("<Configure>", lambda event: self.start_thread())
        self.imageId = self.canvas.create_image(0, 0)
        self.start_thread()
    def condition(self):
            return int(time.time()*10%3)!=1
    def start_thread(self, *args):
        if self.onConfigure:
            return None
        else:
            self.onConfigure = True
            threading.Thread(target=self.relative_resize_image, args=(*args,)).start()
    def relative_resize_image(self, condition=""):
        size = (self.canvas.winfo_width(), self.canvas.winfo_height())
        state = root.state()
        if state!=self.state:
            self.change_size()
            self.state = state
            self.onConfigure = False
            return "Zoomed"
        while 1:
            new_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
            if size==new_size:
                self.change_size()
                break
            else:
                self.change_size()
                size = new_size
            time.sleep(0.01)
        self.onConfigure = False
    def change_size(self):
        image = self.cache[1][1] #[left, now->[index, image], right]
        w, h = image.size #?????????????????????????????????
        sw, sh = self.canvas.winfo_width(), self.canvas.winfo_height() #screen_w screen_h
        if w>sw or h>sh:
            w_scale, h_scale = w/sw, h/sh
            if w_scale>h_scale:
                h = int(h*(sw/w))
                w = int(self.canvas.winfo_width())
            else:
                w = int(w*(sh/h))
                h = int(self.canvas.winfo_height())
        image = ImageTk.PhotoImage(image.resize((w, h)))
        self.label_name.config(text=self.images[self.cache[1][0]].split("/")[-1])
        #label.image = image
        #label.config(image=image)
        self.canvas.image = image
        self.canvas.itemconfig(self.imageId, image=image)
        self.canvas.moveto(self.imageId, self.canvas.winfo_width()/2-w/2, self.canvas.winfo_height()/2-h/2)
    def load_image(self, index):
        index = self.index_proccesser(index)
        image = Image.open(self.images[index])
        return [index, image]
    def index_proccesser(self, index):
        if index>len(self.images)-1:
            return 0
        elif index<0:
            return len(self.images)-1
        else:
            return index
    def switch_image(self, side):
        canvas = self.canvas
        #cache [left, now->[index, image], right]
        if side=="right":
            self.cache[0] = self.cache[1]
            self.cache[1] = self.cache[2]
            self.relative_resize_image()
            self.cache[2] = self.load_image(self.cache[2][0]+1)
        else:
            self.cache[2] = self.cache[1]
            self.cache[1] = self.cache[0]
            self.relative_resize_image()
            self.cache[0] = self.load_image(self.cache[0][0]-1)
##########################################Page 1###########################################################

wrapper_page1 = tk.Frame(root)
page1 = tk.Frame(wrapper_page1)
label_folder_explorer = tk.Label(page1, text = "Choose Folder", font=("Arial", 25))

group_buttons = tk.Frame(page1)
button_explore = tk.Button(group_buttons, text = "???????????????Choose Folder", command=chooseFolder)
button_ok = tk.Button(group_buttons, text="OK", command=OK)
button_exit = tk.Button(group_buttons, text="Exit", command=root.destroy)

#side="top"
wrapper_page1.place(x=0, y=0, relwidth=1, relheight=1)
page1.pack(expand=1)
label_folder_explorer.pack(anchor="center")
group_buttons.pack(anchor="center", pady=10)
button_explore.pack(anchor="w")
button_ok.pack(anchor="w", pady=10)
button_exit.pack(anchor="w")

##########################################Page 2###########################################################
page2 = tk.Frame(root)
ImageManager = None
label_image_name = tk.Label(page2, text = "Choose Folder", font=("Arial", 25))
group_image = tk.Frame(page2)
canvas = tk.Canvas(group_image, bg="black")
button_left = tk.Button(group_image, text = "<", font=("Arial", 25))
button_right = tk.Button(group_image, text = ">", font=("Arial", 25))

page2.place(x=0, y=0, relwidth=1, relheight=1)
label_image_name.pack(anchor="center")
group_image.pack(expand=1, fill="both")
group_image.grid_columnconfigure(1, weight=25)
group_image.grid_columnconfigure(2, weight=1030)
group_image.grid_columnconfigure(3, weight=25)
group_image.grid_rowconfigure(0, weight=100)
button_left.grid(row=0, column=1, sticky="nsew")
canvas.grid(row=0, column=2, sticky="nsew")
button_right.grid(row=0, column=3, sticky="nsew")

wrapper_page1.tkraise()

root.mainloop()
