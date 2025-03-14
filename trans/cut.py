from PIL import Image, ImageOps
import numpy as np

# 1. 打开已经二值化的图像
im = Image.open("two.jpg")
img_array = np.array(im)


# 2. 找到黑色区域的边界坐标
rows = np.any(img_array == 0, axis=1)
cols = np.any(img_array == 0, axis=0)

min_row, max_row = np.where(rows)[0][[0, -1]]
min_col, max_col = np.where(cols)[0][[0, -1]]

print(min_row, min_col)

row_length = max_row - min_row
col_length = max_col - min_col

print(row_length, col_length)

# 3. 裁剪到边界框
cropped_array = img_array[
    min_row : max_row,
    min_col : max_col
]
cropped_img = Image.fromarray(cropped_array)

current_width, current_height = cropped_img.size

target_width = current_width
target_height = target_width * 2

target_size = (target_width, target_height)


resized_img = cropped_img.resize(target_size, resample=Image.LANCZOS)

# 5. 保存结果
resized_img.save("cuted.jpg")
