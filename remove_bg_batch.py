"""
python remove_bg_batch.py <input_dir> <output_dir> [--image_list_file <image_list_file>]
python remove_bg_batch.py D:/Research/ZZB/AssetGenerator/data/demo1/images D:/Research/ZZB/AssetGenerator/data/demo1/masks
"""

import os
from rembg import remove
from PIL import Image

def remove_bg_for_images(input_dir, output_dir, image_list_file=None):
    """
    批量移除图片背景，生成掩码，支持指定图片列表。
    :param input_dir: 原始图片文件夹
    :param output_dir: 掩码输出文件夹
    :param image_list_file: 只处理列表中的图片（可选）
    """
    os.makedirs(output_dir, exist_ok=True)

    if image_list_file:
        with open(image_list_file, 'r', encoding='utf-8') as f:
            image_names = set(line.strip() for line in f if line.strip())
    else:
        image_names = set(os.listdir(input_dir))

    for img_name in image_names:
        input_path = os.path.join(input_dir, img_name)
        output_path = os.path.join(output_dir, img_name + ".png")
        if not os.path.isfile(input_path):
            print(f"跳过不存在的文件: {input_path}")
            continue
        try:
            with Image.open(input_path) as img:
                out = remove(img)
                # 如果图像是 RGBA 模式，转换为 RGB 模式
                if out.mode == "RGBA":
                    out = out.convert("RGB")
                out.save(output_path)
            print(f"已处理: {img_name}")
        except Exception as e:
            print(f"处理失败: {img_name}, 错误: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="批量移除图片背景，生成掩码")
    parser.add_argument("input_dir", type=str, help="原始图片文件夹")
    parser.add_argument("output_dir", type=str, help="掩码输出文件夹")
    parser.add_argument("--image_list_file", type=str, default=None, help="只处理列表中的图片（可选）")
    args = parser.parse_args()
    remove_bg_for_images(args.input_dir, args.output_dir, args.image_list_file)
