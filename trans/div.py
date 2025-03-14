from PIL import Image, ImageEnhance
import numpy as np
import cv2

# 打开图片并转为灰度图
im = Image.open("0.jpg").convert("L")

# 添加锐化处理（可选，根据需求选择是否保留）
enhancer = ImageEnhance.Sharpness(im)
sharpened_im = enhancer.enhance(2.0)  # 锐化强度

# 转为numpy数组并二值化
img_array = np.array(sharpened_im)  # 若不需要锐化，直接用 np.array(im.convert("L"))
threshold = 100
binary_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)

# 定义结构化元素（核）
kernel = np.ones((6, 6), np.uint8)  # 可调整核大小（如5x5）

# 执行开运算：先腐蚀后膨胀
opened_array = cv2.morphologyEx(
    binary_array,  # 输入二值图像数组
    cv2.MORPH_OPEN,  # 操作类型（开运算）
    kernel,  # 结构化元素
)
# 将处理后的数组转为Image对象
result = Image.fromarray(opened_array)

# 保存结果
result.save("two.jpg")
