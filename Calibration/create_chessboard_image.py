import numpy as np
import matplotlib.pyplot as plt
import pathlib

img_size = [2480, 3508]
square_size = 146


image_mat = np.zeros(img_size)

for i in range(image_mat.shape[0]):
    for j in range(image_mat.shape[1]):
        
        x, y = i//square_size, j//square_size

        if (x + y) % 2 == 1:
            image_mat[i, j] = 255


plt.imshow(image_mat)
plt.show()

plt.imsave(str(pathlib.Path().resolve()) + f"/Calibration/{img_size[0]//square_size}x{img_size[1]//square_size}_chessboard.png", image_mat, cmap = 'gray')