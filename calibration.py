# this script is used to find intrinsic and extrinsic parameters of the camera
# intrinsic parameters such as focal length, principal point, and lens distortion
# extrinsic parameters such as position and orientation with respect to each other
# baseline distance between the two cameras
# 

# opencv tutorial: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
# possible calibration patterns
# chessboard (https://github.com/opencv/opencv/blob/4.x/doc/pattern.png)
# asymmetric circles (https://github.com/opencv/opencv/blob/4.x/doc/acircles_pattern.png)
# circles
# grid
# charuco (https://github.com/opencv/opencv/blob/4.x/doc/charuco_board_pattern.png)
# rings (see paper: Accurate Camera Calibration using Iterative Refinement of Control Points)
# pattern generator (https://github.com/opencv/opencv/blob/4.x/doc/pattern_tools/gen_pattern.py)

#TODO: at the momement the script uses chess pattern. Future iterations, explore different calibration patterns

import numpy as np
import cv2
import glob







def find_calibration_corners(images, pattern_size, objp, verbose=False):
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    # termination criteria for refinement of the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #no of images
    n_images = len(images)

    for i, image_path in enumerate(images):

        print(f"Processing image: {i}/{n_images}", end="\r")

        # Read the image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        # If corners are found, add object points and image points
        if ret:
            objpoints.append(objp)
            # Refine the corners
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
        # if verbose mode, draw and display the corners
        if verbose:
            cv2.drawChessboardCorners(image, pattern_size, corners, ret)
            cv2.imshow('image', image)
            cv2.waitKey(500)
    
    # if verbose mode, destroy all image windows that was showing the corners
    if verbose:
        cv2.destroyAllWindows()


    return objpoints, imgpoints



def calibrate_camera(objpoints, imgpoints, image_size, verbose=False):
    # Perform camera calibration
    ret, camera_matrix, distortion_coefficients, _, _ = cv2.calibrateCamera(
        objpoints,
        imgpoints,
        image_size,
        None,
        None
    )
    # if verbose mode print out status
    if verbose:
        print("Camera Calibration is Done. RMS:", ret)

    return camera_matrix, distortion_coefficients

def chessboard_calibration(verbose=False):
    """
    This function is used to calibrate the camera using a chessboard pattern

    saves the camera matrix and distortion coefficients to a file for future use
    """
    
    # calibration setting
    # Number of inner corners in the calibration pattern (width and height)
    pattern_size = (9, 6)

    # Length of the square in your calibration pattern (in any unit)
    square_size = 1.0

    


    # Prepare the object points, e.g., (0,0,0), (1,0,0), (2,0,0), ..., (8,5,0)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp *= square_size

    # Directory containing calibration images
    calibration_image_dir = 'calibration_images/chessboard/*.jpg'
    calibration_images = glob.glob(calibration_image_dir)

    # Find calibration corners in the images
    objpoints, imgpoints = find_calibration_corners(calibration_images, pattern_size, objp, verbose=verbose)


    # Get image size (assuming all images have the same size)
    # check if there are images in the directory
    if len(calibration_images) == 0:
        print("Error: No images found in the calibration directory")
        return
    image = cv2.imread(calibration_images[0])
    image_size = (image.shape[1], image.shape[0])

    # Calibrate the camera
    camera_matrix, distortion_coefficients = calibrate_camera(objpoints, imgpoints, image_size, verbose=verbose)

    # Save the calibration data to a file for future use (e.g., stereo vision)
    calibration_data = {
        'camera_matrix': camera_matrix,
        'distortion_coefficients': distortion_coefficients
    }

    np.savez('calibration_data.npz', **calibration_data)
