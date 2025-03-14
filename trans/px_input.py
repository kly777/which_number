from PIL import Image
import numpy as np
from collections import deque

def pix(img: Image.Image) -> np.ndarray:
    im = img
    im_array: np.ndarray = np.array(im)

    target_height: int = 16
    target_width: int = 8
    row_step: int = im_array.shape[0] // target_height
    col_step: int = im_array.shape[1] // target_width

    result_array: np.ndarray = np.zeros((target_height, target_width), dtype=int)

    for i in range(target_height):
        for j in range(target_width):
            row_start: int = i * row_step
            row_end: int = (i + 1) * row_step
            col_start: int = j * col_step
            col_end: int = (j + 1) * col_step

            block: np.ndarray = im_array[row_start:row_end, col_start:col_end]
            result_array[i, j] = block.min()

    distance_array: np.ndarray = distance_transform(result_array)
    binary_data: np.ndarray = distance_array.astype(float)
    # print(binary_data)
    return binary_data

def distance_transform(arr: np.ndarray) -> np.ndarray:
    rows, cols = arr.shape
    dist: np.ndarray = np.full_like(arr, -1, dtype=int)
    q: deque[tuple[int, int]] = deque()

    # 初始化队列：所有0的位置距离为0
    for i in range(rows):
        for j in range(cols):
            if arr[i, j] == 0:
                dist[i, j] = 0
                q.append((i, j))

    # BFS扩展
    dirs: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四方向
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and dist[ni, nj] == -1:
                dist[ni, nj] = dist[i, j] + 1
                q.append((ni, nj))
    max_value: int = np.max(dist)
    dist: np.ndarray = dist / max_value
    return dist
