import cv2
import numpy as np
from PIL import Image
from src.config import config

camera_frame_view = cv2.imread(config.camera_image_view_path)
bird_eye_view     = cv2.imread(config.bird_view_path)

img_copy = camera_frame_view.copy()

def draw_circle(x, y, flags, param):
    """Draw a circle on the image at the specified coordinates."""
    # Draw a circle at the clicked position
    # cv2.circle(img, (x, y), 30, (0, 255, 0), 3)
    # For a larger circle, you can adjust the radius and color
    # Here, we use a radius of 100 and color (0, 0, 255) for red
    # You can also change the thickness of the circle
    # to -1 to fill the circle
    # or a positive value to draw the circle outline
    # For example, to fill the circle:
    # global img_copy
    # img_copy = cv2.circle(img_copy, (x, y), 50, (0, 255, 0), 3)
    cv2.circle(img_copy, (x, y), 50, (0, 255, 0), 3)
    cv2.imshow("window_name", img_copy) 

    # If you want to draw an outline instead, use a positive thickness
    # img_copy =     
    #cv2.circle((x, y), 100, (0, 255, 0), 5)

def mouse_callback(event, x, y, flags, param):

    """Mouse callback function to handle mouse events."""
    if event == cv2.EVENT_LBUTTONDOWN : #EVENT_LBUTTONDBLCLK:
        # Draw a circle at the clicked position
        draw_circle(x, y, flags, param)

        # cv2.circle(camera_frame_view, (x, y), 30, (0, 255, 0), 3)  
        print(f"Clicked at: ({x}, {y})")

cv2.namedWindow("window_name", cv2.WINDOW_NORMAL) # cv2.WINDOW_NORMAL cv2.WINDOW_GUI_EXPANDED)
cv2.setMouseCallback("window_name", mouse_callback)

if cv2.waitKey(0) == ord("q") :
    cv2.destroyAllWindows()