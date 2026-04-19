#!/usr/bin/env python3
"""
合并多张服装图片为一张（用于虚拟换装）
用法: python combine_garments.py <image1> <image2> [image3...] [--output output.png]
"""

import argparse
from PIL import Image


def combine_garment_images(img_paths, output_path, direction='horizontal'):
    """合并多张服装图片"""
    images = [Image.open(p) for p in img_paths]
    
    if direction == 'horizontal':
        target_height = min(img.height for img in images)
        resized = []
        total_width = 0
        for img in images:
            ratio = target_height / img.height
            new_w = int(img.width * ratio)
            resized.append(img.resize((new_w, target_height), Image.LANCZOS))
            total_width += new_w
        combined = Image.new('RGB', (total_width, target_height))
        x = 0
        for img in resized:
            combined.paste(img, (x, 0))
            x += img.width
    elif direction == 'vertical':
        target_width = min(img.width for img in images)
        resized = []
        total_height = 0
        for img in images:
            ratio = target_width / img.width
            new_h = int(img.height * ratio)
            resized.append(img.resize((target_width, new_h), Image.LANCZOS))
            total_height += new_h
        combined = Image.new('RGB', (target_width, total_height))
        y = 0
        for img in resized:
            combined.paste(img, (0, y))
            y += img.height
    
    combined.save(output_path, quality=95)
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='合并多张服装图片')
    parser.add_argument('images', nargs='+', help='要合并的图片路径')
    parser.add_argument('--output', '-o', default='garment_combined.png', help='输出路径')
    parser.add_argument('--direction', '-d', choices=['horizontal', 'vertical'], default='horizontal', help='合并方向')
    
    args = parser.parse_args()
    result = combine_garment_images(args.images, args.output, args.direction)
    print(f"✅ 合并完成: {result}")
