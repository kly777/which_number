import os
import glob
import numpy as np


def normalize_file(input_path, output_dir):
    """
    对单个文件进行归一化处理并保存结果

    Args:
        input_path (str): 输入文件路径
        output_dir (str): 输出目录路径
    """
    try:
        # 读取数据
        binary_data = np.loadtxt(input_path, dtype=float)

        # 计算最大值并归一化
        max_value = np.max(binary_data)
        normalized_data = binary_data / max_value

        # 创建输出目录（若不存在）
        os.makedirs(output_dir, exist_ok=True)

        # 生成输出文件名
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, f"{filename}")

        # 保存结果
        np.savetxt(output_path, normalized_data, fmt="%.6f", delimiter=" ")
        print(f"处理完成：{input_path} → {output_path}")

    except Exception as e:
        print(f"❌ 处理 {input_path} 失败：{str(e)}")


def batch_process(input_dir="data_back/data", output_dir="data"):
    """
    批量处理指定目录中的所有 .txt 文件

    Args:
        input_dir (str): 输入文件夹路径（默认"data"）
        output_dir (str): 输出文件夹路径（默认"output"）
    """
    # 遍历所有 .txt 文件
    for file_path in glob.glob(os.path.join(input_dir, "*.txt")):
        normalize_file(file_path, output_dir)


if __name__ == "__main__":
    batch_process()
