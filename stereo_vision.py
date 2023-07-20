# main function file for the program

# import statements
import os
from calibration import chessboard_calibration 

# main function
def main():
    # calibrate camera if not already calibrated
    if not os.path.exists("camera_calibration.npz"):
        chessboard_calibration()


# call main function
if __name__ == "__main__":
    main()