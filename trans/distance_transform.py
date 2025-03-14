import numpy as np
from collections import deque
from typing import Tuple

def distance_transform(arr: np.ndarray) -> np.ndarray:
    """
    计算二维数组中每个像素到最近0像素的距离

    Args:
        arr (np.ndarray): 输入二值数组，0表示目标像素

    Returns:
        np.ndarray: 归一化的距离数组
    """
    rows, cols = arr.shape
    dist = np.full_like(arr, -1, dtype=float)
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
    
    # 归一化
    max_value = np.max(dist)
    if max_value > 0:
        dist /= max_value
    return dist