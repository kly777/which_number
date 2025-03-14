from PIL import Image, ImageEnhance
import numpy as np
import cv2

class ImageProcessor:
    def __init__(
        self,
        sharpness: float = 2.0,
        threshold: int = 100,
        kernel_size: tuple[int, int] = (6, 6),
        contrast: float = 2,
    ):
        self.sharpness: float = sharpness
        self.threshold: int = threshold
        self.kernel: np.ndarray = np.ones(kernel_size, np.uint8)
        self.original_img: Image.Image | None = None
        self.processed_img: Image.Image | None = None
        self.contrast: float = contrast

    def load_image(self, path: str) -> None:
        """加载并转换为灰度图"""
        try:
            self.original_img = Image.open(path).convert("L")
        except Exception as e:
            raise ValueError(f"图像加载失败：{str(e)}")

    def enhance_sharpness(self) -> None:
        """应用锐化处理"""
        enhancer = ImageEnhance.Sharpness(self.original_img)
        self.original_img = enhancer.enhance(self.sharpness)

    def binary_threshold(self) -> None:
        """二值化处理"""
        img_array: np.ndarray = np.array(self.original_img)
        # 获取图像最小像素值（最暗部分）
        min_val: int = np.min(img_array)
        lower_threshold: int = min_val
        upper_threshold: int = min_val + 40
        self.binary_array: np.ndarray = np.where(
            (img_array >= lower_threshold) & (img_array <= upper_threshold), 0, 255
        ).astype(np.uint8)
        # print(f"二值化阈值：{self.threshold}")

    def morphology_open(self) -> None:
        """形态学开运算（去噪）"""
        self.opened_array: np.ndarray = cv2.morphologyEx(
            self.binary_array, cv2.MORPH_OPEN, self.kernel
        )
        # print(f"应用开运算，核大小：{self.kernel.shape}")

    def process(self, img_path: str) -> Image.Image:
        """完整处理流程"""
        self.load_image(img_path)
        self.enhance_sharpness()
        self.binary_threshold()
        self.morphology_open()
        self.processed_img = Image.fromarray(self.opened_array)
        return self.processed_img
