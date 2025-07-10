from os import path
import cv2

from config.config import camera_frame_path, camera_video_path
from application.utils import load_image, first_camera_frame

frame = load_image(camera_frame_path)

if frame is None :
    frame = first_camera_frame(camera_video_path)

cv2.imshow("frame", frame)    

if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    
