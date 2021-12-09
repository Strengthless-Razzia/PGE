import numpy as np

def get_calib_params(intrinsic_filename):
    calibration_params = np.loadtxt(open(intrinsic_filename), delimiter=",")

    [alphaU_l, alphaV_l, u0_l, v0_l] = calibration_params

    instrinsic_matrix = np.array([  [alphaU_l, 0, u0_l],
                                    [0, alphaV_l, v0_l],
                                    [0, 0, 1]])

    return instrinsic_matrix



