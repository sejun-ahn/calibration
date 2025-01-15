import cv2
import numpy as np
import os
import json
import argparse

def calibration(video, block_array=(5,8), block_length=30.0):
    size = None
    object_point = np.zeros((block_array[0]*block_array[1],3), np.float32)
    object_point[:,:2] = np.mgrid[0:block_array[0],0:block_array[1]].T.reshape(-1,2)
    object_point *= block_length

    object_points, corners = [], []

    basename = os.path.splitext(os.path.basename(video))[0]
    directory = f"{basename}/frames"
    images = [os.path.join(directory, f) for f in os.listdir(directory)]

    for image in images:
        img = cv2.imread(image)
        if size is None:
            size = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corner = cv2.findChessboardCorners(gray, block_array, None)

        if ret:
            corner2 = cv2.cornerSubPix(gray, corner, (11,11), (-1,-1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            object_points.append(object_point)
            corners.append(corner2)

    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(object_points, corners, gray.shape[::-1], None, None)
    return cameraMatrix, distCoeffs, retval, size

def save(video, cameraMatrix, distCoeffs, retval, size):
    basename = os.path.splitext(os.path.basename(video))[0]
    device, case = basename.split('_')
    data = {
        "device": device,
        "case": case,
        "cameraMatrix": cameraMatrix.reshape(-1).tolist(),
        "distCoeffs": distCoeffs.reshape(-1).tolist(),
        "retval": retval,
        "size": size
    }
    json.dump(data, open(f"{basename}/{basename}.json", "w"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calibration of the camera')
    parser.add_argument('video', type=str, help='path to the video file')
    parser.add_argument('--block_array', type=int, nargs=2, default=(5,8), help='number of blocks in the chessboard')
    parser.add_argument('--block_length', type=float, default=30.0, help='length of each block in mm')
    args = parser.parse_args()

    result = calibration(args.video, args.block_array, args.block_length)
    save(args.video, *result)