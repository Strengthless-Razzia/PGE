# Import required modules
import cv2
import numpy as np
import glob
from PIL import Image 

# Define the dimensions of checkerboard
CHECKERBOARD = (16,23)


# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS + 
			cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# Vector for 3D points
threedpoints = []

# Vector for 2D points
twodpoints = []


# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0]
					* CHECKERBOARD[1],
					3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
							0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None


# Extracting path of individual image stored
# in a given directory. Since no path is
# specified, it will take current directory
# jpg files alone
images = glob.glob('PLAQUE_BOMBEE/calibration/data_2/*.bmp')

for filename in images:
	image = cv2.imread(filename)
	grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	img = Image.open(filename)
	img = img.convert("RGB")
 
	d = img.getdata()
	new_image = []
	for item in d:
		if item == (255,255,255):
			new_image.append((0, 0, 0))
		else:
			new_image.append(item)
	# update image data
	img.putdata(new_image)
	image = np.array(img)
	grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#img.save("grille_altere.jpg")
	
	# Find the chess board corners
	# If desired number of corners are
	# found in the image then ret = true
	ret, corners = cv2.findChessboardCorners(
					grayColor, CHECKERBOARD,
					cv2.CALIB_CB_ADAPTIVE_THRESH>
					+ cv2.CALIB_CB_FAST_CHECK +
					cv2.CALIB_CB_NORMALIZE_IMAGE)

	# If desired number of corners can be detected then,
	# refine the pixel coordinates and display
	# them on the images of checker board
	if ret == True:
		threedpoints.append(objectp3d)

		# Refining pixel coordinates
		# for given 2d points.
		corners2 = cv2.cornerSubPix(
			grayColor, corners, (11, 11), (-1, -1), criteria)

		twodpoints.append(corners2)

		# Draw and display the corners
		image = cv2.drawChessboardCorners(image,
										CHECKERBOARD,
										corners2, ret)

	scale_percent = 50 # percent of original size
	width = int(image.shape[1] * scale_percent / 100)
	height = int(image.shape[0] * scale_percent / 100)
	dim = (width, height)
	
	# resize image
	image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
	cv2.imshow('img', image)
	cv2.waitKey(0)

cv2.destroyAllWindows()

h, w = image.shape[:2]


# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
if ret == True:
	ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, grayColor.shape[::-1], None, None)
	# Displaying required output
	print(" Camera matrix:")
	print(matrix)

	print("\n Distortion coefficient:")
	print(distortion)

	print("\n Rotation Vectors:")
	print(r_vecs)

	print("\n Translation Vectors:")
	print(t_vecs)
else:
	print("Chessboard not detected")