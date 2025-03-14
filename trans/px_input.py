import numpy as np
from collections import deque


def pix(img):
    im = img
    im_array = np.array(im)

    target_height = 16
    target_width = 8
    row_step = im_array.shape[0] // target_height
    col_step = im_array.shape[1] // target_width

    result_array = np.zeros((target_height, target_width), dtype=int)

    for i in range(target_height):
        for j in range(target_width):
            row_start = i * row_step
            row_end = (i + 1) * row_step
            col_start = j * col_step
            col_end = (j + 1) * col_step

            block = im_array[row_start:row_end, col_start:col_end]
            result_array[i, j] = block.min()

    distance_array = distance_transform(result_array)
    binary_data = distance_array.astype(float)
    # print(binary_data)
    return binary_data


def distance_transform(arr):
    rows, cols = arr.shape
    dist = np.full_like(arr, -1, dtype=int)
    q = deque()

    # 初始化队列：所有0的位置距离为0
    for i in range(rows):
        for j in range(cols):
            if arr[i, j] == 0:
                dist[i, j] = 0
                q.append((i, j))

    # BFS扩展
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四方向
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and dist[ni, nj] == -1:
                dist[ni, nj] = dist[i, j] + 1
                q.append((ni, nj))
    max_value = np.max(dist)
    dist = dist / max_value
    return dist
