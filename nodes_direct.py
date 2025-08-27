"""
ComfyUI Popo Utility - 直接节点实现
完全兼容ComfyUI的标准格式
"""

import torch
import numpy as np


class PopoImageSizeNode:
    """获取图片长边和短边尺寸的节点"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("long_side", "short_side")
    FUNCTION = "get_image_size"
    CATEGORY = "popo-utility"
    
    def get_image_size(self, image):
        """获取图片尺寸"""
        try:
            # 从PyTorch张量获取尺寸
            if len(image.shape) == 4:  # [batch, height, width, channels]
                height, width = image.shape[1], image.shape[2]
            elif len(image.shape) == 3:  # [height, width, channels]
                height, width = image.shape[0], image.shape[1]
            else:
                return (0, 0)
            
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (long_side, short_side)
        except Exception as e:
            print(f"PopoImageSizeNode error: {e}")
            return (0, 0)


class PopoImageDimensionsNode:
    """获取图片详细尺寸信息的节点"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "long_side", "short_side")
    FUNCTION = "get_dimensions"
    CATEGORY = "popo-utility"
    
    def get_dimensions(self, image):
        """获取图片详细尺寸信息"""
        try:
            # 从PyTorch张量获取尺寸
            if len(image.shape) == 4:  # [batch, height, width, channels]
                height, width = image.shape[1], image.shape[2]
            elif len(image.shape) == 3:  # [height, width, channels]
                height, width = image.shape[0], image.shape[1]
            else:
                return (0, 0, 0, 0)
            
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (width, height, long_side, short_side)
        except Exception as e:
            print(f"PopoImageDimensionsNode error: {e}")
            return (0, 0, 0, 0)


class PopoImageAspectRatioNode:
    """计算图片宽高比的节点"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("aspect_ratio", "ratio_name")
    FUNCTION = "calculate_aspect_ratio"
    CATEGORY = "popo-utility"
    
    def calculate_aspect_ratio(self, image):
        """计算图片宽高比"""
        try:
            # 从PyTorch张量获取尺寸
            if len(image.shape) == 4:  # [batch, height, width, channels]
                height, width = image.shape[1], image.shape[2]
            elif len(image.shape) == 3:  # [height, width, channels]
                height, width = image.shape[0], image.shape[1]
            else:
                return (0.0, "invalid")
            
            if height == 0 or width == 0:
                return (0.0, "invalid")
            
            # 计算宽高比
            aspect_ratio = width / height
            
            # 识别常见比例
            ratio_name = self._identify_common_ratio(aspect_ratio)
            
            return (round(aspect_ratio, 3), ratio_name)
        except Exception as e:
            print(f"PopoImageAspectRatioNode error: {e}")
            return (0.0, "error")
    
    def _identify_common_ratio(self, ratio):
        """识别常见的宽高比名称"""
        common_ratios = {
            1.0: "1:1 Square",
            4/3: "4:3 Standard",
            3/2: "3:2 Classic",
            16/9: "16:9 Widescreen",
            21/9: "21:9 Ultrawide",
            5/4: "5:4 Monitor",
            3/4: "3:4 Portrait Standard",
            2/3: "2:3 Portrait Classic",
            9/16: "9:16 Portrait Widescreen",
        }
        
        # 容差范围
        tolerance = 0.05
        
        for target_ratio, name in common_ratios.items():
            if abs(ratio - target_ratio) <= tolerance:
                return name
        
        # 判断横屏还是竖屏
        if ratio > 1:
            return f"{ratio:.2f}:1 Landscape"
        else:
            return f"1:{1/ratio:.2f} Portrait"


# ComfyUI需要的映射
NODE_CLASS_MAPPINGS = {
    "PopoImageSizeNode": PopoImageSizeNode,
    "PopoImageDimensionsNode": PopoImageDimensionsNode,
    "PopoImageAspectRatioNode": PopoImageAspectRatioNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PopoImageSizeNode": "Popo Image Size",
    "PopoImageDimensionsNode": "Popo Image Dimensions", 
    "PopoImageAspectRatioNode": "Popo Image Aspect Ratio",
}

# 打印加载信息
print("Popo Utility: Direct ComfyUI nodes loaded successfully!")
print(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes in 'popo-utility' category")