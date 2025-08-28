"""
ComfyUI Popo Utility - 直接节点实现
完全兼容ComfyUI的标准格式
"""

import torch
import numpy as np
import math
import re


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


class PopoMathExpressionNode:
    """数学表达式计算节点"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0, "min": -999999, "max": 999999, "step": 0.01}),
                "b": ("FLOAT", {"default": 0.0, "min": -999999, "max": 999999, "step": 0.01}),
                "c": ("FLOAT", {"default": 0.0, "min": -999999, "max": 999999, "step": 0.01}),
                "expression": ("STRING", {"multiline": False, "default": "a + b + c"}),
            }
        }
    
    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("result_int", "result_float")
    FUNCTION = "calculate_expression"
    CATEGORY = "popo-utility"
    
    def calculate_expression(self, a, b, c, expression):
        """计算数学表达式"""
        try:
            # 安全的数学函数白名单
            safe_functions = {
                # 基础数学函数
                'abs': abs,
                'round': round,
                'int': int,
                'float': float,
                'min': min,
                'max': max,
                'pow': pow,
                
                # math模块函数
                'ceil': math.ceil,
                'floor': math.floor,
                'sqrt': math.sqrt,
                'exp': math.exp,
                'log': math.log,
                'log10': math.log10,
                'log2': math.log2,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'atan2': math.atan2,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'asinh': math.asinh,
                'acosh': math.acosh,
                'atanh': math.atanh,
                'degrees': math.degrees,
                'radians': math.radians,
                'fabs': math.fabs,
                'factorial': math.factorial,
                'gcd': math.gcd,
                'lcm': getattr(math, 'lcm', lambda x, y: abs(x * y) // math.gcd(x, y)),
                
                # 数学常数
                'pi': math.pi,
                'e': math.e,
                'tau': math.tau,
                'inf': math.inf,
                'nan': math.nan,
            }
            
            # 创建安全的执行环境
            safe_dict = {
                '__builtins__': {},
                'a': float(a),
                'b': float(b), 
                'c': float(c),
                **safe_functions
            }
            
            # 验证表达式安全性
            if not self._is_safe_expression(expression):
                raise ValueError("表达式包含不安全的操作")
            
            # 计算表达式
            result = eval(expression, safe_dict)
            
            # 确保结果是数字
            if not isinstance(result, (int, float, complex)):
                raise ValueError("表达式结果必须是数字")
            
            # 处理复数
            if isinstance(result, complex):
                if result.imag == 0:
                    result = result.real
                else:
                    raise ValueError("不支持复数结果")
            
            # 处理特殊值
            if math.isnan(result):
                result = 0.0
            elif math.isinf(result):
                result = 999999.0 if result > 0 else -999999.0
            
            result_float = float(result)
            result_int = int(result_float)
            
            return (result_int, result_float)
            
        except Exception as e:
            print(f"PopoMathExpressionNode error: {e}")
            return (0, 0.0)
    
    def _is_safe_expression(self, expression):
        """检查表达式是否安全"""
        # 禁止的关键词和操作
        forbidden_patterns = [
            r'import\s+',
            r'__.*__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'vars\s*\(',
            r'dir\s*\(',
            r'getattr\s*\(',
            r'setattr\s*\(',
            r'hasattr\s*\(',
            r'delattr\s*\(',
            r'callable\s*\(',
            r'isinstance\s*\(',
            r'issubclass\s*\(',
            r'super\s*\(',
            r'type\s*\(',
            r'classmethod\s*\(',
            r'staticmethod\s*\(',
            r'property\s*\(',
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, expression, re.IGNORECASE):
                return False
        
        return True


# ComfyUI需要的映射
NODE_CLASS_MAPPINGS = {
    "PopoImageSizeNode": PopoImageSizeNode,
    "PopoImageDimensionsNode": PopoImageDimensionsNode,
    "PopoImageAspectRatioNode": PopoImageAspectRatioNode,
    "PopoMathExpressionNode": PopoMathExpressionNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PopoImageSizeNode": "Popo Image Size",
    "PopoImageDimensionsNode": "Popo Image Dimensions", 
    "PopoImageAspectRatioNode": "Popo Image Aspect Ratio",
    "PopoMathExpressionNode": "Popo Math Expression",
}

# 打印加载信息
print("Popo Utility: Direct ComfyUI nodes loaded successfully!")
print(f"Registered {len(NODE_CLASS_MAPPINGS)} nodes in 'popo-utility' category")
for node_name in NODE_CLASS_MAPPINGS.keys():
    print(f"  - {node_name}")