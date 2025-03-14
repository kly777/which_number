import os
from glob import glob
from PIL import Image
from trans.cut2 import ImageProcessor as ImageCut
from trans.div2 import ImageProcessor as ImageDiv
from trans.px_data2 import pxify


def batch_process_images(input_dir="raw_img", output_dir="data"):
    """
    批量处理 rawimg 文件夹中的所有 JPG 文件

    Args:
        input_dir (str): 输入文件夹路径（默认"rawimg"）
        output_dir (str): 输出文件夹路径（默认"output"）
    """
    # 创建输出目录（若不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有 JPG 文件
    image_paths = glob(os.path.join(input_dir, "*.jpg"))
    if not image_paths:
        raise FileNotFoundError(f"未找到 {input_dir} 中的 JPG 文件")

    # 初始化处理器
    div_processor = ImageDiv(
        sharpness=2.0,  # 锐化强度（0.5~3.0）
        threshold=90,  # 二值化阈值（0~255）
        kernel_size=(6, 6),  # 形态学核大小
    )

    image_cut = ImageCut(
        target_ratio=0.5, resample=Image.NEAREST  # 宽高比1:2  # 使用最近邻插值
    )

    # 遍历处理每个文件
    for input_path in image_paths:
        # 获取文件名（不含扩展名）
        filename = os.path.splitext(os.path.basename(input_path))[0]+"r"
        print(f"处理文件：{input_path}")

        try:
            # 1. 分割与形态学处理
            dived_img = div_processor.process(input_path)

            # 2. 裁剪和调整尺寸
            cuted_img = image_cut.process(dived_img)

            # 3. 生成最终数据文件
            output_prefix = os.path.join(output_dir, filename)
            pxify(cuted_img, output_prefix)  # 假设 pxify 接受输出前缀

            print(f"完成：{output_prefix}.txt")

        except Exception as e:
            print(f"❌ 处理 {input_path} 失败：{str(e)}")


if __name__ == "__main__":
    batch_process_images()
