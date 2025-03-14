from PIL import Image, ImageEnhance
import numpy as np
import cv2


class ImageProcessor:
    def __init__(
        self,
        sharpness=2.0,
        threshold=100,
        kernel_size=(6, 6),
        contrast=2,
    ):
        self.sharpness = sharpness
        self.threshold = threshold
        self.kernel = np.ones(kernel_size, np.uint8)
        self.original_img = None
        self.processed_img = None
        self.contrast = contrast

    def load_image(self, path):
        """加载并转换为灰度图"""
        try:
            self.original_img = Image.open(path).convert("L")

        except Exception as e:
            raise ValueError(f"图像加载失败：{str(e)}")

    def enhance_sharpness(self):
        """应用锐化处理"""
        # enhancer = ImageEnhance.Contrast(self.original_img)
        # self.original_img = enhancer.enhance(self.contrast)
        enhancer = ImageEnhance.Sharpness(self.original_img)
        self.original_img = enhancer.enhance(self.sharpness)

    def binary_threshold(self):
        """二值化处理"""
        img_array = np.array(self.original_img)
        # 获取图像最小像素值（最暗部分）
        min_val = np.min(img_array)
        lower_threshold = min_val
        upper_threshold = min_val + 40
        self.binary_array = np.where(
            (img_array >= lower_threshold) & (img_array <= upper_threshold), 0, 255
        ).astype(np.uint8)
        # print(f"二值化阈值：{self.threshold}")

    def morphology_open(self):
        """形态学开运算（去噪）"""
        self.opened_array = cv2.morphologyEx(
            self.binary_array, cv2.MORPH_OPEN, self.kernel
        )
        # print(f"应用开运算，核大小：{self.kernel.shape}")

    # def save_result(self):
    #     """保存处理结果"""
    #     if self.processed_img:
    #         self.processed_img.save(self.output_path)
    #         print(f"结果已保存至：{self.output_path}")
    #     else:
    #         raise ValueError("请先执行处理流程")

    def process(self, img_path):
        """完整处理流程"""
        self.load_image(img_path)
        self.enhance_sharpness()
        self.binary_threshold()
        self.morphology_open()
        self.processed_img = Image.fromarray(self.opened_array)
        return self.processed_img
