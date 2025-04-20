from PIL import Image
import numpy as np
from .distance_transform import distance_transform


def pix(img: Image.Image) -> np.ndarray:
    """
    将图像转换为16x8的归一化距离数组
    """
    # 转换为numpy数组
    im_array = np.array(img)

    # 目标尺寸
    target_height = 16
    target_width = 8

    # 计算步长
    row_step = im_array.shape[0] // target_height
    col_step = im_array.shape[1] // target_width

    # 初始化结果数组
    result_array = np.zeros((target_height, target_width), dtype=int)

    # 使用向量化操作处理像素块
    for i in range(target_height):
        for j in range(target_width):
            row_start = i * row_step
            row_end = (i + 1) * row_step
            col_start = j * col_step
            col_end = (j + 1) * col_step

            # 取当前块的最小值
            block = im_array[row_start:row_end, col_start:col_end]
            result_array[i, j] = block.min()

    # 计算距离变换并返回
    return distance_transform(result_array)
