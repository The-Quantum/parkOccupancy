import cv2
import sys
import numpy as np
from src.config.config import coordinate_file

def draw_circle(envent, x, y, img, flags, param):

    if envent == cv2.EVENT_LBUTTONDBLCLK :
        cv2.circle(img, (x, y), 100, 0, 0, -1)

def show_img(image_path:str) :

    try :
        img = cv2.imread(image_path)
    except Exception as e:
        print(f"""The image : {image_path} not found or failed to load.
            The following exception {e}. This has made the application 
            to stop. Please provide the right image path and run the 
            application again."""
        )
        sys.exit(0)

    while True :

        cv2.imshow("Parking frame", img) 
        if cv2.waitKey(500) == ord("q") :
            break
    
    cv2.destroyAllWindows()

class CoordinateGenerator :
    
    KEY_QUIT = ord("q")

    def __init__(self, image_path):

        self.image   = cv2.imread(image_path)

        if self.image is None:
            raise ValueError(f"""Image at {image_path} could not be loaded. 
                Please check the path.""")
        
        if self.image.dtype != 'uint8':
            print(f"""self.image.dtype = {self.image.dtype}, and size = {self.image.shape} """)
            self.image = ( 255 * self.image ).astype('uint8')

        self.image_processed = self.image.copy()
        
        self.window_name = "Parking Frame" 
        self.FRAME_OPEN = True

        self.coordinates = []
        self.click_count = 0
        self.slot_id = 0
    
    def generate_coordinate(self) :

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL) #cv2.WINDOW_GUI_EXPANDED)
        #cv2.setMouseCallback(self.window_name, self._mouse_callback)

        while self.FRAME_OPEN :

            cv2.setMouseCallback(self.window_name, self._mouse_callback)
            key = cv2.waitKey(0)

            if key == CoordinateGenerator.KEY_QUIT:
                self.FRAME_OPEN = False
                cv2.destroyAllWindows()
                break

        cv2.destroyAllWindows()
    
    def _mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN :

            self.coordinates.append( (x, y) ) 
            self.click_count += 1

            if self.click_count > 1 :
                self._draw_line()
            
            if self.click_count == 4 :
                self._save_coordinates()
                
                self.click_count = 0
                self.slot_id += 1
            
            print(f"Coordinates: {self.coordinates}, clic count: {self.click_count}, slot id: {self.slot_id}")
        
        cv2.imshow(self.window_name, self.image_processed) 
                
    def _handle_rectangle(self) :

        cv2.rectangle(
            self.image_processed, self.coordinates[-4], self.coordinates[-2], 
            (0, 255, 0), 2
        )
        
    def _draw_line(self):

        # Draw a line between the last two coordinates
        cv2.line(
            self.image_processed, self.coordinates[-2], 
            self.coordinates[-1], (0, 0, 255), 2
        )
        if self.click_count == 4:
            # Draw a line between the first and the last coordinates
            # to close the rectangle
            cv2.line(
                self.image_processed, self.coordinates[-4], 
                self.coordinates[-1], (0, 0, 255), 2
            )  

    def _save_coordinates(self):

        coordinates_array = np.array(self.coordinates)
        
        coordinates_str = "{ id: " + str( self.slot_id ) + ", coordinates: [" + \
            "[" + str(coordinates_array[0][0]) + "," + str(coordinates_array[0][1]) + "]," + \
            "[" + str(coordinates_array[1][0]) + "," + str(coordinates_array[1][1]) + "]," + \
           "[" + str(coordinates_array[2][0]) + "," + str(coordinates_array[2][1]) + "]," + \
            "[" + str(coordinates_array[3][0]) + "," + str(coordinates_array[3][1]) + "]] } \n"

        with open(coordinate_file, "a") as f:             
            f.write( coordinates_str )
 