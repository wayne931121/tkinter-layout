import tkinter as tk
root = tk.Tk()
root.title("Example"); scale=1.8;
root.geometry("{}x{}+450+300".format(int(360*scale), int(200*scale)))

class scrollFrame(tk.Frame):
    def __init__(self, **options):
        outerFrame = tk.Frame(root)
        canvas = tk.Canvas(outerFrame, highlightthickness=0)
        super().__init__(canvas, **options)
        vsb = tk.Scrollbar(outerFrame, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=1, anchor="nw")
        wrapFrameId = canvas.create_window((0,0), window=self, anchor="nw")
        canvas.config(yscrollcommand=vsb.set)
        canvas.bind("<Configure>", lambda event: self.onFrameConfigure())
        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)) # on mouse enter
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>")) # on mouse leave
        self.outerFrame, self.canvas, self.vsb, self.wrapFrameId = outerFrame, canvas, vsb, wrapFrameId
    def onFrameConfigure(self):
        canvas = self.canvas
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(self.wrapFrameId, width=canvas.winfo_width())
    def on_mouse_wheel(self, event, scale=3):
        canvas = self.canvas
        #only care event.delta is - or +, scroll down or up
        if event.delta<0:
            canvas.yview_scroll(scale, "units")
        else:
            canvas.yview_scroll(-scale, "units")

frame = scrollFrame(bg="#FFFFFF")
frame.outerFrame.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.8)
frame.grid_columnconfigure(0, weight=1)
for i in range(100):
    tk.Button(frame, text=str(i)).grid()
tk.Button(frame, text=str(i)).place(relx=0.25, rely=0.5, relwidth=0.5)


root.mainloop()





























def RelativePositionChange(canvas, ItemId):
    x1, y1, x2, y2 = canvas.bbox(ItemId)
    width, height = canvas.winfo_width(), canvas.winfo_height()
    center, half_w, half_h = [(x1+x2)/2/width, (y1+y2)/2/height], (x2-x1)/2, (y2-y1)/2
    while 1:
       new_x, new_y = canvas.winfo_width()*center[0], canvas.winfo_height()*center[1]
       canvas.moveto(ItemId, new_x-half_w, new_y-half_h)
       yield None

class RelativePositionAndSizeChange:
    def __init__(self, canvas):
        self.canvas, self.Previous_Width, self.Previous_Height = canvas, 0, 0
    def __call__(self, event):
        canvas = self.canvas
        new_w, new_h = canvas.winfo_width(), canvas.winfo_height()
        if self.Previous_Width>0 and self.Previous_Height>0: #Have Recorded
            x_scale, y_scale = new_w/self.Previous_Width, new_h/self.Previous_Height
            canvas.scale("all", event.x, event.y, x_scale, y_scale)
        self.Previous_Width, self.Previous_Height = new_w, new_h


#c_Relative = RelativePositionChange(c, ItemID1)
#c.bind("<Configure>", lambda event: next(c_Relative))