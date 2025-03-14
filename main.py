from glob import glob
import os
from PIL import Image
from trans.px_input import pix
from diff import compare_all_files
import numpy as np

from image_utils import create_image_processors, process_image

# 创建图像处理对象
div_processor, processor = create_image_processors()


def process_images(input_dir: str) -> None:
    """
    处理指定目录中的所有图像文件。

    Args:
        input_dir (str): 输入图像文件的目录路径。
    """
    image_paths: list[str] = glob(os.path.join(input_dir, "*"))
    if not image_paths:
        raise FileNotFoundError(f"未找到 {input_dir} 中的 JPG 文件")

    for image_path in image_paths:
        # 使用工具函数处理图像
        cuted_img: Image.Image = process_image(image_path, div_processor, processor)

        # 转换为像素数组
        input_array: np.ndarray = pix(cuted_img)

        # 比较所有文件
        result: list[tuple[str, float]] = compare_all_files(input_array)

        # 按数值升序排序
        sorted_result: list[tuple[str, float]] = sorted(result, key=lambda x: x[1])
        top: list[tuple[str, float]] = sorted_result[:4]

        # 输出结果
        print(f"与{image_path.split('/')[-1]}最匹配的4个结果：")
        score: dict[str, float] = {str(i): 0 for i in range(10)}
        for i, entry in enumerate(top, 1):
            label: str = entry[0][0]  # 提取标签（如'0.txt' → '0'）
            print(f" {i} ：文件名：{entry[0]}，值：{entry[1]}，判断为{label}")
            # 计算权重
            score[label] += (11 - i) / (entry[1] + 0.00000001)

        # 根据最小值推断结果（取第一个最小的文件名首字符）
        best_label: str = max(score, key=score.get)
        print(f"最终推断结果：它是 {best_label}\n")


# 处理raw_img目录中的图像
process_images("raw_img")