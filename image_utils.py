from PIL import Image
from trans.cut2 import ImageCut
from trans.div2 import ImageDiv


def create_image_processors():
    """创建并返回图像处理对象"""
    div_processor = ImageDiv(
        sharpness=2.0,  # 锐化强度（0.5~3.0）
        threshold=90,  # 二值化阈值（0~255）
        kernel_size=(6, 6),  # 形态学核大小
    )

    cut_processor = ImageCut(
        target_ratio=0.5,  # 宽高比1:2
        resample=Image.NEAREST,  # 使用最近邻插值
    )

    return div_processor, cut_processor


def process_image(image_path, div_processor, cut_processor):
    """
    处理单个图像文件

    Args:
        image_path (str): 图像文件路径
        div_processor (ImageDiv): 分割处理器
        cut_processor (ImageCut): 裁剪处理器

    Returns:
        Image.Image: 处理后的图像
    """
    # 1. 分割与形态学处理
    dived_img = div_processor.process(image_path)

    # 2. 裁剪和调整尺寸
    cuted_img = cut_processor.process(dived_img)

    return cuted_img
