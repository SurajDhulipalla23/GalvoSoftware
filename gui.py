import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Melanoma  Image Viewer")
        temp = 5
        
        # Create a frame to hold the image
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # self.image_frame.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.image_frame, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load and display the image
        self.load_image('cq5dam.web.1280.1280.jpeg')

        self.classification(temp)
        
        # Create a button to save the image
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.SE)

        

    def classification(self, img): 
        
        canc = False
        # color thresholding 
        # edge thresholding 

        if canc:
            self.red_frame = tk.Frame(bd=0, highlightthickness=0, background="red")
            self.red_frame.place(x=0, y=0, relwidth=0.5, relheight=1, anchor="nw")
            # Create a label to display "CANCEROUS"
            self.label = tk.Label(self.root, text="CANCEROUS", font=('Helvetica', 24))
            self.label.pack(side=tk.LEFT, padx=20, pady=20)
        else:
            self.green_frame = tk.Frame(bd=0, highlightthickness=0, background="green")
            self.green_frame.place(x=0, y=0, relwidth=0.5, relheight=1, anchor="nw")
            # Create a label to display "CANCEROUS"
            self.label = tk.Label(self.root, text="NOT CANCEROUS", font=('Helvetica', 24))
            self.label.pack(side=tk.LEFT, padx=20, pady=20)

    def load_image(self, filename):
        self.image = Image.open(filename)
        self.image = self.image.resize((400, 400), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
    
    def save_image(self):
        # Ask user to choose file location for saving
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        
        # Save the image
        if filename:
            self.image.save(filename)
            print("Image saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
