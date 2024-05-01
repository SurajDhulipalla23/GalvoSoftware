import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui as pg
import time

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Melanoma Image Viewer")
            
        # Create a frame to hold the image
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # self.image_frame.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.image_frame, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a label to display "Please load an image"
        self.placeholder_label = tk.Label(self.image_frame, text="Please load an image", font=('Arial', 24))
        self.placeholder_label.pack(expand=True)
        
        # Load and display the default image
        # default_image_path = 'cq5dam.web.1280.1280.jpeg'
        # self.load_image(default_image_path)
        self.classification(1)
        # Create a button to load a new image
        self.load_button = tk.Button(self.root, text="Load Image", command=self.open_image)
        self.load_button.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.NW)

        # Create a button to save the image
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.SE)

        self.timestamp_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.timestamp_label.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.SW)

        # Update the timestamp label every second
        self.update_timestamp()
        

    def classification(self, img): 
        canc = False

        if canc:
            self.red_frame = tk.Frame(bd=0, highlightthickness=0, background="red")
            self.red_frame.place(x=0, y=0, relwidth=0.5, relheight=1, anchor="nw")
            # Create a label to display "CANCEROUS"
            self.label = tk.Label(self.root, text="CANCEROUS", font=('Arial', 24))
            self.label.pack(side=tk.LEFT, padx=20, pady=20)
        else:
            self.green_frame = tk.Frame(bd=0, highlightthickness=0, background="green")
            self.green_frame.place(x=0, y=0, relwidth=0.5, relheight=1, anchor="nw")
            # Create a label to display "CANCEROUS"
            self.label = tk.Label(self.root, text="NOT CANCEROUS", font=('Arial', 24))
            self.label.pack(side=tk.LEFT, padx=20, pady=20)

    def load_image(self, filename):
        self.image = Image.open(filename)
        self.image = self.image.resize((400, 400), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            # Remove the placeholder label and display the image
            self.placeholder_label.pack_forget()
            self.load_image(file_path)
            # self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def save_image(self):
        x, y = self.root.winfo_rootx(), self.root.winfo_rooty()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        screenshot = pg.screenshot(filename, region=(x, y, w, h))
        if filename:
            screenshot.save(filename)
            print("Screenshot saved successfully.")

    def update_timestamp(self):
        # Update the timestamp label with the current time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=timestamp)
        # Schedule the update every second
        self.root.after(1000, self.update_timestamp)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
