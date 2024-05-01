# gui.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from logic import ImageLogic
import time

class GUIApp:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic

        self.root.title("Melanoma Image Viewer")

        self.gui_frame = tk.Frame(self.root)
        self.gui_frame.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.gui_frame)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.placeholder_label = tk.Label(self.image_frame, text="Please load an image", font=('Arial', 24))
        self.placeholder_label.pack(expand=True)

        self.canvas = tk.Canvas(self.image_frame, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.image_frame, text="Load Image", command=self.open_image)
        self.load_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.save_button = tk.Button(self.image_frame, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.timestamp_label = tk.Label(self.image_frame, text="", font=('Arial', 12))
        self.timestamp_label.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.S)
        self.update_timestamp()

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            image = self.logic.load_image(file_path)
            self.show_image(image)

    def show_image(self, image):
        # Display the image on the canvas
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        # Update classification label
        self.update_classification_label()

    def update_classification_label(self):
        if self.logic.classification:
            classification_label = tk.Label(self.image_frame, text=self.logic.classification, font=('Arial', 24))
            classification_label.pack(padx=20, pady=20)

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            image = self.canvas.itemcget(self.canvas.find_all()[0], 'image')
            self.logic.save_image(image, filename)
            print("Screenshot saved successfully.")

    def update_timestamp(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=timestamp)
        self.root.after(1000, self.update_timestamp)

if __name__ == "__main__":
    root = tk.Tk()
    logic = ImageLogic()
    app = GUIApp(root, logic)
    root.mainloop()
