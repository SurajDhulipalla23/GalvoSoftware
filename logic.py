# logic.py
from tkinter import filedialog
from PIL import Image

class ImageLogic:
    def __init__(self):
        self.classification = None

    def load_image(self, file_path):
        image = Image.open(file_path)
        # Perform classification logic
        self.classification = self.classify(image)
        return image

    def classify(self, image):
        # Perform classification logic here
        # For demonstration purposes, let's assume it's always not cancerous
        return "NOT CANCEROUS"

    def save_image(self, image, filename):
        image.save(filename)