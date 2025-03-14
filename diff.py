import numpy as np
import os


def subtract_and_sum(a, b):
    """
    计算二维数组a中值为0的位置，与b数组对应位置相减后的总和。

    Args:
        a (np.ndarray): 输入数组A（二维）
        b (np.ndarray): 输入数组B（二维）

    Returns:
        int: 所有符合条件的差值之和
    """
    # 确保输入是NumPy数组
    a = np.array(a)
    b = np.array(b)

    # 检查维度匹配
    if a.shape != b.shape:
        raise ValueError("数组维度不匹配")

    mask_a = a == 0
    result_a = np.sum((b[mask_a] ** 5))

    mask_b = b == 0
    result_b = np.sum((a[mask_b] ** 5))

    return result_a + result_b + (result_a - result_b) ** 2


def read_txt_to_array(file_path):
    """读取txt文件为二维数组"""
    try:
        return np.loadtxt(file_path, dtype=float)
    except Exception as e:
        raise ValueError(f"文件读取失败: {file_path}\n{str(e)}")


def compare_all_files(a, data_dir="data"):
    """
    逐个比较data文件夹中的txt文件与输入数组a

    Args:
        a (np.ndarray): 输入数组
        data_dir (str): 存放txt文件的目录路径

    Returns:
        list: [(文件名, 比较结果), ...]
    """
    results = []

    # 遍历目录中的所有txt文件
    for root, _, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                try:
                    b = read_txt_to_array(file_path)
                    result = subtract_and_sum(a, b)
                    results.append((filename, result))
                    # print(f"文件 {filename}：结果 = {result}")
                except Exception as e:
                    print(f"处理 {filename} 失败：{str(e)}")

    return results
