from PIL import Image, ImageOps, ImageFilter
import numpy as np
from collections import deque


def distance_transform(arr):
    rows, cols = arr.shape
    dist = np.full_like(arr, -1,dtype=int)
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
    return dist


im = Image.open("cuted.jpg")
im_array = np.array(im)

target_height = 16
target_width = 8
row_step = im_array.shape[0] // target_height
col_step = im_array.shape[1] // target_width

result_array = np.zeros((target_height, target_width), dtype=np.uint8)

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

binary_data = distance_array.astype(int)

np.savetxt("binary.txt", binary_data, fmt="%d", delimiter=" ")

# binary_data = np.loadtxt("binary.txt", dtype=int)

# # 验证形状（例如：16x8）
# print("数组形状:", binary_data.shape)
# print("示例内容:\n", binary_data[:2, :2])
