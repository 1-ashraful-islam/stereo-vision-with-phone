# main function file for the program

# import statements
import os
import numpy as np
import argparse
from calibration import chessboard_calibration 

# main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Stereo Vision using phone cameras")
    parser.add_argument("--v", help="verbose mode", action="store_true")
    args = parser.parse_args()

    # calibration data file
    calibration_data_file = "calibration_data.npz"
    # calibrate camera if not already calibrated
    if not os.path.exists(calibration_data_file):
        chessboard_calibration(verbose=args.v)
    
    # load camera matrix and distortion coefficients
    npzfile = np.load(calibration_data_file)
    camera_matrix = npzfile["camera_matrix"]
    distortion_coefficients = npzfile["distortion_coefficients"]

    # print camera matrix and distortion coefficients in verbose mode
    if args.v:
        print("Camera Matrix:\n", camera_matrix)
        print("Distortion Coefficients:\n", distortion_coefficients)

    #


# call main function
if __name__ == "__main__":
    main()