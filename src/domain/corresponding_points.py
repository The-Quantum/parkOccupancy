import cv2
import numpy as np
import json
from PIL import Image
from src.config import config

class PointsCorrespondance:

    KEY = ord("q")
    
    def __init__(self, camera_view_image_path, bird_eye_view_image_path):
        """Initialize with paths to camera view and bird's eye view images."""
        self.camera_image_view   = cv2.imread(camera_view_image_path)
        self.bird_eye_view_image = cv2.imread(bird_eye_view_image_path)

        self.normal_view_points = []
        self.bird_eye_points = []

        if self.camera_image_view is None :
            raise ValueError(f"""Image at {camera_view_image_path} could not be loaded. 
                Please check the path.""")
        if self.bird_eye_view_image is None :
            raise ValueError(f"""Image at {bird_eye_view_image_path} could not be loaded. 
                Please check the path.""")
        
        self.CAMERA_WINDOW_NAME   = "Normal Camera View"
        self.BIRD_EYE_WINDOW_NAME = "Bird's Eye View"
        self.FRAME_OPEN : bool = True
    
    def collect_coordinates(self):

        cv2.namedWindow(self.CAMERA_WINDOW_NAME, cv2.WINDOW_GUI_NORMAL) #cv2.WINDOW_GUI_EXPANDED WINDOW_NORMAL)
        cv2.namedWindow(self.BIRD_EYE_WINDOW_NAME, cv2.WINDOW_GUI_NORMAL) #cv2.WINDOW_GUI_EXPANDED WINDOW_NORMAL)

        while self.FRAME_OPEN :
            cv2.setMouseCallback(self.CAMERA_WINDOW_NAME, self._mouse_callback, param=self.CAMERA_WINDOW_NAME)
            cv2.setMouseCallback(self.BIRD_EYE_WINDOW_NAME, self._mouse_callback, param=self.BIRD_EYE_WINDOW_NAME)

            key = cv2.waitKey(0)

            if key == PointsCorrespondance.KEY:
                reformate_coordinates = self.reformate_coordinates()
                print("Collected points:", reformate_coordinates)
                self.save_points()
                self.FRAME_OPEN = False
                cv2.destroyAllWindows()
                break

    def _mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            """Handle mouse click events to collect coordinates."""
            if param == self.CAMERA_WINDOW_NAME:
                self.normal_view_points.append((x, y))
                self._draw_circle(self.camera_image_view, x, y, full=True)  # Draw filled circle for normal view
                self._draw_circle(self.camera_image_view, x, y, full=False)  # Draw unfilled circle for reference
                self._put_test(self.camera_image_view, f"{len(self.normal_view_points)}", x, y)
                

            elif param == self.BIRD_EYE_WINDOW_NAME:
                self.bird_eye_points.append((x, y))
                self._draw_circle(self.bird_eye_view_image, x, y, full=True)
                self._draw_circle(self.bird_eye_view_image, x, y, full=False)
                self._put_test(self.bird_eye_view_image, f"{len(self.bird_eye_points)}", x, y)
                
        cv2.imshow(self.CAMERA_WINDOW_NAME, self.camera_image_view)
        cv2.imshow(self.BIRD_EYE_WINDOW_NAME, self.bird_eye_view_image)
        
    def _draw_circle(self, img, x, y, full=True):    
        """Draw a circle at the clicked point."""
        if full:
            cv2.circle(img, (x, y), 10, (150, 100, 0), -1) # filled circle
        else:
            cv2.circle(img, (x, y), 30, (255, 0, 255), 8) # unfilled circle
       
    
    def _put_test(self, image, text, x, y):
        """Put text on the image at specified coordinates."""

        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (x, y-15)
        font_scale = 3
        font_thickness = 4
        color = (255, 0, 0)
        cv2.putText(image, text, position, font, font_scale, color, font_thickness)

    def save_points(self):

        points_correspondance = self.reformate_coordinates()
        #json_data = json.dumps(points_correspondance, indent=4)
        """Save the collected points to a file."""
        with open(config.points_correspondance_file, 'w') as f:
            #json.dumps(self.reformate_coordinates(), f)
            f.write("{\n")
            for i, (key, value) in enumerate(points_correspondance.items()):

                comma = "," if i < len(points_correspondance) - 1 else ""
                f.write(f'  "{key}": {json.dumps(value)}{comma}\n')
            f.write("}")

        print("Coordinates saved successfully.")

    def reformate_coordinates(self):
        """Reformat the collected coordinates for further processing."""
        if len(self.normal_view_points) != len(self.bird_eye_points):
            raise ValueError("The number of points in both views must be the same.")
        
        point_correspondance_dict = {}
        for i in range( len(self.normal_view_points) ) :
            points = (self.normal_view_points[i], self.bird_eye_points[i])
            point_correspondance_dict[str(i)] = points            
        
        return point_correspondance_dict
        
        print(f"Collected {len(self.points)} pairs of points.")    
camera_view_image_path   = config.camera_image_view_path
bird_eye_view_image_path = config.bird_view_path

GeneratePoints = PointsCorrespondance(camera_view_image_path, bird_eye_view_image_path)
GeneratePoints.collect_coordinates()