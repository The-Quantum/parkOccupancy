import cv2
import numpy as np

data_file = "../../data/data_file.txt"

def draw_contours(image,
    coordinates, label, font_color,
    border_color=(255, 0, 0),
    line_thickness=1,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=0.5):

    cv2.drawContours(
        image, [coordinates], 
        contourIdx=-1, color=border_color, 
        thickness=2, ineType=cv2.LINE_8
    )
    
    moments = cv2.moments(coordinates)

    center = (
        int(moments["m10"] / moments["m00"]) - 3,
        int(moments["m01"] / moments["m00"]) + 3
    )

    cv2.putText(
        image, label, center, font, font_scale, 
        font_color, line_thickness, cv2.LINE_AA
    )

class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = cv2.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        cv2.namedWindow(self.caption, cv2.WINDOW_GUI_EXPANDED)
        cv2.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            cv2.imshow(self.caption, self.image)
            key = cv2.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        cv2.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.__handle_done()

            elif self.click_count > 1:
                self.__handle_click_progress()

        cv2.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        cv2.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

    def __handle_done(self):
        cv2.line(
            self.image, self.coordinates[2], self.coordinates[3], self.color, 1 
            )
        cv2.line(
            self.image, self.coordinates[3], self.coordinates[0], self.color, 1)

        self.click_count = 0

        coordinates = np.array(self.coordinates)

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                        "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                        "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                        "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                        "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids + 1), (255, 255, 255))

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1

#coordinate_file = "../../data/parking_place_coordinates.json"
image_path = str("../../data/camera_frame.png")

if image_path is not None:

    with open(data_file, "w+") as points:
        generator = CoordinatesGenerator(image_path, points, (255, 0, 0))
        generator.generate()