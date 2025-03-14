from glob import glob
import os
from trans.cut2 import ImageProcessor as ImageCut
from PIL import Image
from trans.div2 import ImageProcessor as ImageDiv
from trans.px_input import pix
from diff import compare_all_files
import numpy as np

# 创建图像处理对象
div_processor: ImageDiv = ImageDiv(
    sharpness=1.0,  # 锐化强度（0.5~3.0）
    threshold=110,  # 二值化阈值（0~255）
    kernel_size=(6, 6),  # 形态学核大小
)

processor: ImageCut = ImageCut(
    target_ratio=0.5,  # 宽高比1:2
    resample=Image.NEAREST,  # 使用最近邻插值
)

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
        # 应用图像处理流程
        dived_img: Image.Image = div_processor.process(image_path)
        cuted_img: Image.Image = processor.process(dived_img)

        # 转换为像素数组
        input_array: np.ndarray = pix(cuted_img)

        # 比较所有文件
        result: list[tuple[str, float]] = compare_all_files(input_array)

        # 按数值升序排序
        sorted_result: list[tuple[str, float]] = sorted(result, key=lambda x: x[1])
        top: list[tuple[str, float]] = sorted_result[:4]

        # 输出结果
        print(f"对于{image_path.split('/')[-1]}最匹配的4个结果：")
        score: dict[str, float] = {str(i): 0 for i in range(10)}
        for i, entry in enumerate(top, 1):
            label: str = entry[0][0]  # 提取标签（如'0.txt' → '0'）
            print(f" {i} ：文件名：{entry[0]}，值：{entry[1]}，判断为{label}")
            # 计算权重（越靠前的排名，权重越高）
            score[label] += (11 - i) / (
                entry[1] + 0.00000001
            )  # 例如第1名权重100，第6名权重25

        # 根据最小值推断结果（取第一个最小的文件名首字符）
        best_label: str = max(score, key=score.get)
        print(f"最终推断结果：它是 {best_label}\n")

# 处理raw_img目录中的图像
process_images("raw_img")
