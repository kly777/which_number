import numpy as np
from .distance_transform import distance_transform


def pxify(img, name):
    im = img
    im_array = np.array(im)

    target_height = 16
    target_width = 8
    row_step = im_array.shape[0] // target_height
    col_step = im_array.shape[1] // target_width

    result_array = np.zeros((target_height, target_width), dtype=float)

    for i in range(target_height):
        for j in range(target_width):
            row_start = i * row_step
            row_end = (i + 1) * row_step
            col_start = j * col_step
            col_end = (j + 1) * col_step

            # 取当前块的最大值
            block = im_array[row_start:row_end, col_start:col_end]
            result_array[i, j] = block.min()

    print(result_array)

    # 2. 计算到最近0的距离
    distance_array = distance_transform(result_array)

    print("", distance_array)

    binary_data = distance_array.astype(float)

    np.savetxt(name + ".txt", binary_data, fmt="%f", delimiter=" ")
