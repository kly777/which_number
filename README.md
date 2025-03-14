# 项目概述

这是一个用于从图像中识别 0-9 的 Python 项目。

## 目录结构

-   `data/`：存放数据文件
-   `kit/`：包含辅助脚本
-   `raw_img/`：存放原始图像文件
-   `trans/`：包含图像处理脚本

## 主要文件

-   `get_data.py`：用于获取数据
-   `main.py`：主程序入口
-   `diff.py`：用于比较图像差异
-   `trans/div2.py`：用于二值化图像
-   `trans/cut2.py`：用于裁剪图像
-   `trans/px-data.py` 和 `trans/px-input.py`：用于处理图片为低像素数组数据

## 使用方法

1. 确保已安装所有依赖项（可以使用以下命令安装这些依赖项：pip install -r requirements.txt）
2. 将待识别图片放入 `raw_img/` 目录下，可以放入多个图片
3. 运行 `main.py` 启动程序，结果会由控制台输出

## 依赖项

-   Pillow
-   numpy
-   cv2