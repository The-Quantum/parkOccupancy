import argparse
from src.config import config
from src.domain.generate_condinates import show_img, CoordinateGenerator

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--image", type=str, required=False, 
        default=config.camera_frame_path,
        dest="image_path",
        help="Provide the image path to locate parking place on"               
    )

    return parser.parse_args()


def main() :

    args = parse_args()
    #show_img(args.image_path)

    Generator = CoordinateGenerator(args.image_path)
    Generator.generate_coordinate()

if __name__ == "__main__" :
    main()
    #args = parse_args()
    #Generator = CoordinateGenerator(args.image_path)
    #Generator.generate_coordinate()