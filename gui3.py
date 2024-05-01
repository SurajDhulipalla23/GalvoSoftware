import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui as pg
import time

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Melanoma Image Viewer")

        # Create a frame to hold the entire GUI
        self.gui_frame = tk.Frame(self.root)
        self.gui_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame to hold the classification information

        # Create a frame to hold the image
        self.image_frame = tk.Frame(self.gui_frame)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a label to display "Please load an image"
        self.placeholder_label = tk.Label(self.image_frame, text="Please load an image", font=('Arial', 24))
        self.placeholder_label.pack(expand=True)

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.image_frame, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and display the default image
        # default_image_path = 'cq5dam.web.1280.1280.jpeg'
        # self.load_image(default_image_path)

        # Create a button to load a new image
        self.load_button = tk.Button(self.image_frame, text="Load Image", command=self.open_image)
        self.load_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Create a button to save the image
        self.save_button = tk.Button(self.image_frame, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Create a label to display the timestamp
        self.timestamp_label = tk.Label(self.image_frame, text="", font=('Arial', 12))
        self.timestamp_label.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.S)
        
        # Update the timestamp label every second
        self.update_timestamp()

    def classification(self, img):
        if img>0:
            self.red_frame = tk.Frame(self.classification_frame, bd=0, highlightthickness=0, background="red")
            self.red_frame.pack(fill=tk.BOTH, expand=True)
            # Create a label to display "CANCEROUS"
            self.label = tk.Label(self.red_frame, text="CANCEROUS", font=('Arial', 24), anchor=tk.CENTER)
            self.label.pack(fill=tk.BOTH, padx=20, pady=20)
        else:
            self.green_frame = tk.Frame(self.classification_frame, bd=0, highlightthickness=0, background="green")
            self.green_frame.pack(fill=tk.BOTH, expand=True)
            # Create a label to display "NOT CANCEROUS"
            self.label = tk.Label(self.green_frame, text="NOT CANCEROUS", font=('Arial', 24))
            self.label.pack(fill=tk.BOTH, padx=20, pady=20, anchor=tk.CENTER)

    def load_image(self, filename):
        self.image = Image.open(filename)
        self.image = self.image.resize((400, 400), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.classification(1)

    def open_image(self):
        # if name:
        #     file_path = name
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            if hasattr(self, 'classification_frame'):
                self.classification_frame.destroy()

            self.classification_frame = tk.Frame(self.gui_frame, bd=1, relief=tk.RAISED)
            self.classification_frame.pack(side=tk.LEFT, fill=tk.Y)
            # Load the image
            self.load_image(file_path)
            # Remove the placeholder label
            self.placeholder_label.pack_forget()

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
