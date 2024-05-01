import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui as pg
import time

import cv2
import numpy as np
from skimage import feature, measure
import matplotlib.pyplot as plt
import os

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

    def load_imageCalc(self, image_path):
    # """Load the image from the path."""
        return cv2.imread(image_path)

    def preprocess_image(self, image):
        """Convert image to grayscale and blur it."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        return blur

    def segment_image(self, image):
        """Apply thresholding to segment the image."""
        _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresholded

    def detect_edges(self, image):
        """Use Canny edge detector to find edges in the image."""
        edges = cv2.Canny(image, 100, 200)
        return edges

    def analyze_edges(self, edges, original_image):
        """Analyze the contours, focusing on the one nearest the center of the image."""
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image_center = np.array(original_image.shape[1::-1]) / 2  # (width, height) / 2 to get center

        # Find contour closest to the center of the image
        min_distance = float('inf')
        closest_contour = None
        for contour in contours:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                # Calculate centroid of the contour
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                centroid = np.array([cx, cy])

                # Calculate the Euclidean distance from the centroid to the center of the image
                distance = np.linalg.norm(centroid - image_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

        if closest_contour is not None:
            # Draw the closest contour on the original image
            cv2.drawContours(original_image, [closest_contour], -1, (0, 255, 0), 3)

            # Calculate perimeter and area
            perimeter = cv2.arcLength(closest_contour, True)
            area = cv2.contourArea(closest_contour)
            if area == 0:
                return "Irregular"

            # Calculate circularity
            circularity = 4 * np.pi * (area / (perimeter**2))
            print(f"Circularity: {circularity}")

            # Plot the image with the contour
            # plt.figure(figsize=(6, 6))
            # plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            # plt.show()

            return "Regular" if circularity > 0.4 else "Irregular"

    def plot_results(self, original, edges):
        """Plot the original and edge-detected images."""
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.title('Original Image')
        plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        plt.subplot(122)
        plt.title('Edge Detected')
        plt.imshow(edges, cmap='gray')
        plt.show()

    def compute_circularity(self, edges, original_image):
        """Compute the circularity of the lesion in the image."""
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image_center = np.array(original_image.shape[1::-1]) / 2

        min_distance = float('inf')
        closest_contour = None
        for contour in contours:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centroid = np.array([cx, cy])
                distance = np.linalg.norm(centroid - image_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

        if closest_contour is not None:
            perimeter = cv2.arcLength(closest_contour, True)
            area = cv2.contourArea(closest_contour)
            if area > 0:
                circularity = 4 * np.pi * (area / (perimeter**2))
                return circularity
        return None

    def classification(self, input):
        if input[0] == "Irregular":
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
        self.image = self.image.resize((400, 400), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        out = self.logic(filename)
        # print(out[1])
        # self.edges_frame = tk.Frame(self.gui_frame)
        # self.edges_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # self.canvas2 = tk.Canvas(self.edges_frame, bg='white', width=400, height=400)
        # self.canvas2.pack(fill=tk.BOTH, expand=True)
        # self.image2 = Image.open(filename)
        # self.image2 = self.image2.resize((400, 400), Image.LANCZOS)
        # self.edges = ImageTk.PhotoImage(self.image2)
        # self.canvas2.create_image(0, 0, anchor=tk.SW, image=self.edges)
        self.classification(out)

    def logic(self, filen):
        circularities = []
        regular = 0
        irregular = 0
        
        image = self.load_imageCalc(filen)
        # image_path = '/Users/surajdhulipalla/Documents/SeniorSpring/BME436/GalvoSoftware/SkinCancerDiagnostic/melanoma_cancer_dataset/test/malignant/melanoma_10106.jpg'
        # image = self.load_imageCalc(image_path)
        preprocessed_image = self.preprocess_image(image)
        segmented_image = self.segment_image(preprocessed_image)
        edges = self.detect_edges(segmented_image)
        edge_type = self.analyze_edges(edges, image)
        self.plot_results(image, edges)
        print(f"The edges are classified as: {edge_type}")
        return edge_type, edges

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
            # self.logic(file_path)
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