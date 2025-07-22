from os import path

PRESENT_DIR = path.dirname(path.realpath(__file__)) 

camera_frame_path = path.join(
    PRESENT_DIR, "../../data/camera_frame.png"
)

camera_video_path = path.join(
    PRESENT_DIR, 
    "../../data/2020-03-19-08-00-00_scene_0013_BB_write.avi"
)

coordinate_file = path.join(
    PRESENT_DIR, "../../data/parking_place_coordinates.json"
)

data_file_path = path.join(
    PRESENT_DIR, "../../data/data_file.txt"
)

camera_image_view_path = path.join(
    PRESENT_DIR, "../../data/IMG_20250711_163748.jpg" #"../../data/camera_image_view.png"
)

bird_view_path = path.join(
    PRESENT_DIR, "../../data/IMG_20250711_163552.jpg" #, ../../data/field_to_view.png"
)