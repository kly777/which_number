from glob import glob
import os
from trans.cut2 import ImageProcessor as ImageCut
from PIL import Image, ImageOps
from trans.div2 import ImageProcessor as ImageDiv
from trans.px_input import pix
from diff import compare_all_files

div_processor = ImageDiv(
    sharpness=1.0,  # 锐化强度（0.5~3.0）
    threshold=110,  # 二值化阈值（0~255）
    kernel_size=(6, 6),  # 形态学核大小
)


processor = ImageCut(
    target_ratio=0.5,  # 宽高比1:2
    resample=Image.NEAREST,  # 使用最近邻插值
)


def jud(input_dir):
    image_paths = glob(os.path.join(input_dir, "*"))
    if not image_paths:
        raise FileNotFoundError(f"未找到 {input_dir} 中的 JPG 文件")
    for image_path in image_paths:
        dived_img = div_processor.process(image_path)
        # 执行完整流程
        cuted_img = processor.process(dived_img)

        # cuted_img.save("cuted.jpg")

        input_array = pix(cuted_img)

        result = compare_all_files(input_array)

        # 按数值升序排序
        sorted_result = sorted(result, key=lambda x: x[1])
        top = sorted_result[:4]

        # 输出结果
        print(f"对于{image_path.split("\\")[1]}最匹配的4个结果：")
        score = {str(i): 0 for i in range(10)}
        for i, entry in enumerate(top, 1):
            label = entry[0][0]  # 提取标签（如'0.txt' → '0'）
            print(f" {i} ：文件名：{entry[0]}，值：{entry[1]}，判断为{label}")
            # 计算权重（越靠前的排名，权重越高）
            score[label] += (11 - i) / (
                entry[1] + 0.00000001
            )  # 例如第1名权重100，第6名权重25

        # 根据最小值推断结果（取第一个最小的文件名首字符）
        best_label = max(score, key=score.get)

        print(f"最终推断结果：它是 {best_label}\n")


jud("raw_img")
