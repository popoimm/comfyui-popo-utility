"""
ComfyUI Popo Utility - 图片处理工具节点
包含图片尺寸获取、分析等功能的节点
"""

from .base_node import ImageProcessingNode
from typing import Tuple


class ImageSizeNode(ImageProcessingNode):
    """
    获取图片长边和宽边尺寸的节点
    输入一张图片，输出该图片的长边和宽边尺寸
    """
    
    DESCRIPTION = "获取图片的长边和短边尺寸，性能优化版本"
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("long_side", "short_side")
    FUNCTION = "get_image_size"
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义输入类型"""
        return {
            "required": {
                "image": ("IMAGE",),  # ComfyUI 标准图片输入
            }
        }
    
    def get_image_size(self, image):
        """
        获取图片尺寸的核心函数
        
        Args:
            image: ComfyUI 格式的图片张量
        
        Returns:
            tuple: (长边尺寸, 短边尺寸)
        """
        if not self.validate_inputs(image=image):
            return (0, 0)
        
        try:
            width, height = self.get_image_dimensions(image)
            
            if width == 0 or height == 0:
                return (0, 0)
            
            # 计算长边和短边
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (long_side, short_side)
            
        except Exception as e:
            self.log_error(e, "get_image_size")
            return (0, 0)


class ImageDimensionsNode(ImageProcessingNode):
    """
    获取图片详细尺寸信息的节点
    输出宽度、高度、长边、短边四个值
    """
    
    DESCRIPTION = "获取图片的详细尺寸信息：宽度、高度、长边、短边"
    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "long_side", "short_side")
    FUNCTION = "get_dimensions"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    def get_dimensions(self, image):
        """
        获取图片详细尺寸信息
        
        Args:
            image: ComfyUI 格式的图片张量
        
        Returns:
            tuple: (宽度, 高度, 长边, 短边)
        """
        if not self.validate_inputs(image=image):
            return (0, 0, 0, 0)
        
        try:
            width, height = self.get_image_dimensions(image)
            
            if width == 0 or height == 0:
                return (0, 0, 0, 0)
            
            # 计算长边和短边
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (width, height, long_side, short_side)
            
        except Exception as e:
            self.log_error(e, "get_dimensions")
            return (0, 0, 0, 0)


class ImageAspectRatioNode(ImageProcessingNode):
    """
    计算图片宽高比的节点
    输出浮点数宽高比和常见比例名称
    """
    
    DESCRIPTION = "计算图片的宽高比和识别常见比例类型"
    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("aspect_ratio", "ratio_name")
    FUNCTION = "calculate_aspect_ratio"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    def calculate_aspect_ratio(self, image):
        """
        计算图片宽高比
        
        Args:
            image: ComfyUI 格式的图片张量
        
        Returns:
            tuple: (宽高比浮点数, 比例名称字符串)
        """
        if not self.validate_inputs(image=image):
            return (0.0, "unknown")
        
        try:
            width, height = self.get_image_dimensions(image)
            
            if width == 0 or height == 0:
                return (0.0, "invalid")
            
            # 计算宽高比
            aspect_ratio = width / height
            
            # 识别常见比例
            ratio_name = self._identify_common_ratio(aspect_ratio)
            
            return (round(aspect_ratio, 3), ratio_name)
            
        except Exception as e:
            self.log_error(e, "calculate_aspect_ratio")
            return (0.0, "error")
    
    def _identify_common_ratio(self, ratio: float) -> str:
        """识别常见的宽高比名称"""
        common_ratios = {
            1.0: "1:1 (正方形)",
            4/3: "4:3 (标准)",
            3/2: "3:2 (经典)",
            16/9: "16:9 (宽屏)",
            21/9: "21:9 (超宽屏)",
            5/4: "5:4 (显示器)",
            3/4: "3:4 (竖屏标准)",
            2/3: "2:3 (竖屏经典)",
            9/16: "9:16 (竖屏宽屏)",
        }
        
        # 容差范围
        tolerance = 0.05
        
        for target_ratio, name in common_ratios.items():
            if abs(ratio - target_ratio) <= tolerance:
                return name
        
        # 判断横屏还是竖屏
        if ratio > 1:
            return f"{ratio:.2f}:1 (横屏)"
        else:
            return f"1:{1/ratio:.2f} (竖屏)"


# 导出节点类
NODE_CLASSES = [
    ImageSizeNode,
    ImageDimensionsNode,
    ImageAspectRatioNode,
]