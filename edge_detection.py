import cv2
import numpy as np
from skimage import feature, measure
import matplotlib.pyplot as plt
import os

def load_image(image_path):
    """Load the image from the path."""
    return cv2.imread(image_path)

def preprocess_image(image):
    """Convert image to grayscale and blur it."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

def segment_image(image):
    """Apply thresholding to segment the image."""
    _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresholded

def detect_edges(image):
    """Use Canny edge detector to find edges in the image."""
    edges = cv2.Canny(image, 100, 200)
    return edges

# def analyze_edges(edges, original_image):
#     """Analyze the contours and check the smoothness of edges."""
#     contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]  # get the largest contour
#     for cnt in contours:
#         cv2.drawContours(original_image, [cnt], -1, (0, 255, 0), 3)
#         perimeter = cv2.arcLength(cnt, True)
#         area = cv2.contourArea(cnt)
#         if area == 0:
#             return "Irregular"
#         circularity = 4*np.pi*(area/(perimeter**2))
#         print(circularity)
#         # Plot the image with the contour
#         plt.figure(figsize=(6, 6))
#         plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
#         plt.show()
#         return "Regular" if circularity > 0.4 else "Irregular"
def analyze_edges(edges, original_image):
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

def plot_results(original, edges):
    """Plot the original and edge-detected images."""
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.subplot(122)
    plt.title('Edge Detected')
    plt.imshow(edges, cmap='gray')
    plt.show()

def compute_circularity(edges, original_image):
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

def process_images_from_folder(folder_path, type = "malignant"):
    circularities = []
    regular = 0
    irregular = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            image = load_image(file_path)
            if image is not None:
                preprocessed_image = preprocess_image(image)
                segmented_image = segment_image(preprocessed_image)
                edges = detect_edges(segmented_image)
                edge_type = analyze_edges(edges, image)
                if edge_type == "Regular":
                    regular = regular + 1
                if edge_type == "Irregular":
                    irregular = irregular + 1
                # plot_results(image, edges)
                # print(f"The edges for image {file_path} are classified as: {edge_type}")
                circularity = compute_circularity(edges, image)
                if circularity is not None:
                    circularities.append(circularity)
    return circularities, regular, irregular

# Paths to the folders
path_malignant = '/Users/surajdhulipalla/Documents/SeniorSpring/BME436/GalvoSoftware/SkinCancerDiagnostic/melanoma_cancer_dataset/test/malignant/'
path_benign = '/Users/surajdhulipalla/Documents/SeniorSpring/BME436/GalvoSoftware/SkinCancerDiagnostic/melanoma_cancer_dataset/test/benign/'

# Process images and compute statistics
circularities_malignant, regular_malignant, irregular_malignant = process_images_from_folder(path_malignant, "malignant")
circularities_benign, regular_benign, irregular_benign = process_images_from_folder(path_benign, "benign")

mean_circularity_malignant = np.mean(circularities_malignant)
std_dev_circularity_malignant = np.std(circularities_malignant)
mean_circularity_benign = np.mean(circularities_benign)
std_dev_circularity_benign = np.std(circularities_benign)

print("Malignant Lesions:")
print("Number of Regular = {} and Number of Irregular = {}".format(regular_malignant, irregular_malignant))
print(f"Mean Circularity: {mean_circularity_malignant}")
print(f"Standard Deviation of Circularity: {std_dev_circularity_malignant}")

print("Benign Lesions:")
print("Number of Regular = {} and Number of Irregular = {}".format(regular_benign, irregular_benign))
print(f"Mean Circularity: {mean_circularity_benign}")
print(f"Standard Deviation of Circularity: {std_dev_circularity_benign}")

# plt.hist(circularities_malignant, bins = 20)
plt.hist(circularities_benign, bins = 20)
plt.show()

# Main workflow
# image_path = '/Users/surajdhulipalla/Documents/SeniorSpring/BME436/GalvoSoftware/SkinCancerDiagnostic/melanoma_cancer_dataset/test/malignant/melanoma_10106.jpg'
# image = load_image(image_path)
# preprocessed_image = preprocess_image(image)
# segmented_image = segment_image(preprocessed_image)
# edges = detect_edges(segmented_image)
# edge_type = analyze_edges(edges, image)
# plot_results(image, edges)
# print(f"The edges are classified as: {edge_type}")
