import numpy as np

with open('HoleDetection/Points2D/clicked_points_TestMatching.npy', 'rb') as f:
        clicked_points = np.load(f, allow_pickle=False)


print(np.floor(clicked_points))

