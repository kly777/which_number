from PIL import Image
import numpy as np

class ImageProcessor:
    def __init__(self, target_ratio: float = 1 / 2, resample: int = Image.LANCZOS):
        """
        图像处理类初始化

        Args:
            target_ratio (float): 目标宽高比（默认1:2）
            resample (int): 缩放插值方法（默认Image.LANCZOS）
        """
        self.target_ratio: float = target_ratio
        self.resample: int = resample
        self.original_img: Image.Image | None = None
        self.cropped_img: Image.Image | None = None
        self.resized_img: Image.Image | None = None

    def load_image(self, img: Image.Image) -> None:
        """加载并验证输入图像"""
        try:
            self.original_img = img
            self.img_array: np.ndarray = np.array(self.original_img)
            # print(f"成功加载图像，尺寸：{self.original_img.size}")
        except Exception as e:
            raise ValueError(f"图像加载失败：{str(e)}")

    def find_bounding_box(self) -> tuple[int, int, int, int]:
        """定位黑色区域边界"""
        rows: np.ndarray = np.any(self.img_array == 0, axis=1)
        cols: np.ndarray = np.any(self.img_array == 0, axis=0)

        # 获取边界坐标
        min_row, max_row = np.where(rows)[0][[0, -1]]
        min_col, max_col = np.where(cols)[0][[0, -1]]

        # 计算尺寸
        self.row_length: int = max_row - min_row
        self.col_length: int = max_col - min_col

        # print(f"边界坐标：min_row={min_row}, min_col={min_col}")
        # print(f"区域尺寸：row_length={self.row_length}, col_length={self.col_length}")

        return (min_row, max_row, min_col, max_col)

    def crop_image(self) -> None:
        """根据边界坐标裁剪图像"""
        min_row, max_row, min_col, max_col = self.find_bounding_box()
        cropped_array: np.ndarray = self.img_array[min_row:max_row, min_col:max_col]
        self.cropped_img = Image.fromarray(cropped_array)
        # print(f"裁剪后尺寸：{self.cropped_img.size}")

    def resize_image(self) -> None:
        """调整图像到目标宽高比"""
        if self.cropped_img is None:
            raise ValueError("请先执行裁剪操作")

        current_width, current_height = self.cropped_img.size
        # 计算目标尺寸（以宽度为基准）
        target_width: int = current_width
        target_height: int = int(target_width / self.target_ratio)  # 根据宽高比计算

        self.resized_img = self.cropped_img.resize(
            (target_width, target_height), resample=self.resample
        )
        # print(f"调整后尺寸：{self.resized_img.size}")

    def process(self, img: Image.Image) -> Image.Image:
        """完整处理流程"""
        self.load_image(img)
        self.crop_image()
        self.resize_image()
        return self.resized_img
