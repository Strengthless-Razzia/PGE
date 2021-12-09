from PNL_implementation import PNL
from utils import get_calib_params
from manualLineDetection.manual_line_detection import select_segments
import numpy as np


edges_file_path = './data_plaques/Plaque_1.edges'
points_file_path = './data_plaques/Plaque_1.xyz'
image_path = './Photos plaques/CognexInsight5100/capture1.jpg'
nb_segments = 4

intrinsic_matrix_unity = get_calib_params('./Calibration/calib_simulation/calibration_parameters.txt')
#lol

#intrinsic_matrix = np.array([   [2.60607474e+03, 0.00000000e+00, 2.21400822e+02],
#                                [0.00000000e+00, 2.24540967e+03, 4.43022384e+02],
#                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
#

#intrinsic_matrix = np.array([   [1.96906639e+03, 0.00000000e+00, 2.45375293e+02],
#                                [0.00000000e+00, 1.94755972e+03, 4.84719674e+02],
#                                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

intrinsic_matrix_5100  = get_calib_params('./Calibration/calib_simulation/calibration_parameters_5100.txt')

print(intrinsic_matrix_5100)

if __name__ == '__main__':
    

    pick_lines_Ro, normal_vectors, model3D_Ro =  select_segments(nb_segments, intrinsic_matrix_5100, image_path, points_file_path, edges_file_path)

    pnl = PNL(nb_segments, pick_lines_Ro, normal_vectors, model3D_Ro, intrinsic_matrix_5100)

    pnl.run(image_path)


## position=(0.0, 4900.0, -3000.0)_rotation=(60.0, 0.0, 15.0)
##[[-9.66418241e-01  2.25749524e-01 -1.22771883e-01  4.52615169e+00]
## [-2.56856161e-01 -8.34114893e-01  4.88136515e-01 -1.46576404e+01]
## [ 7.79072963e-03  5.03278747e-01  8.64089004e-01  5.78470688e+02]
## [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]

## position=(1000.0, 8000.0, -3000.0)_rotation=(60.0, 0.0, 15.0)
## [[-9.64272961e-01  2.25056606e-01 -1.39739688e-01 -1.29735710e+02]
##  [-2.64816521e-01 -8.32974689e-01  4.85824431e-01  1.11199107e+02]
##  [-7.06162592e-03  5.05472741e-01  8.62813677e-01  8.45157082e+02]
##  [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]