import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'GX020050_frame_38759.jpg'  
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image
plt.figure(figsize=(6, 6))
plt.imshow(image_rgb)
plt.title("Original Image")
plt.axis('off')
plt.show()

# Apply Gaussian smoothing
gaussian_blur = cv2.GaussianBlur(image_rgb, (5, 5), 0)

# Convert to HSV color space
image_hsv = cv2.cvtColor(gaussian_blur, cv2.COLOR_RGB2HSV)

# Identify green areas of the field
lower_green = np.array([30, 40, 40])
upper_green = np.array([90, 255, 255])
mask = cv2.inRange(image_hsv, lower_green, upper_green)

# Display the mask image
plt.figure(figsize=(6, 6))
plt.imshow(mask, cmap='gray')
plt.title("Mask of the Field")
plt.axis('off')
plt.show()

# Find the largest contour
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ensure at least one contour was found
if contours:
    # Assume the largest contour is the field
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    field_image = image_rgb[y:y+h, x:x+w]

    # Display the cropped image
    plt.figure(figsize=(6, 6))
    plt.imshow(field_image)
    plt.title("Cropped Field Image")
    plt.axis('off')
    plt.show()
else:
    print("No contours found. Check the threshold values and image processing steps.")
