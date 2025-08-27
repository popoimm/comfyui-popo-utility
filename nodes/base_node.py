"""
ComfyUI Popo Utility - 节点基础类
为所有自定义节点提供统一的接口和功能
"""

from typing import Dict, Any, Tuple, List, Optional


class PopoBaseNode:
    """
    Popo工具集节点的基础类
    所有自定义节点都应该继承这个类
    """
    
    # 节点元数据
    CATEGORY = "popo-utility"
    DESCRIPTION = "Popo工具集基础节点"
    
    def __init__(self):
        self.node_id = self.__class__.__name__
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """
        定义节点的输入类型
        子类应该重写此方法
        """
        return {"required": {}}
    
    def get_node_info(self) -> Dict[str, Any]:
        """
        获取节点的完整信息
        用于注册和调试
        """
        return {
            "class_name": self.__class__.__name__,
            "category": getattr(self.__class__, 'CATEGORY', 'popo-utility'),
            "description": getattr(self.__class__, 'DESCRIPTION', ''),
            "input_types": self.__class__.INPUT_TYPES(),
            "return_types": getattr(self.__class__, 'RETURN_TYPES', ()),
            "return_names": getattr(self.__class__, 'RETURN_NAMES', ()),
            "function": getattr(self.__class__, 'FUNCTION', ''),
        }
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """
        统一的错误日志记录
        """
        error_msg = f"[{self.node_id}] 错误"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        print(error_msg)
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        输入验证的通用方法
        子类可以重写此方法来添加自定义验证
        """
        return True


class ImageProcessingNode(PopoBaseNode):
    """
    图片处理节点的基础类
    为图片处理相关的节点提供通用功能
    """
    
    CATEGORY = "popo-utility/image"
    
    def get_image_dimensions(self, image) -> Tuple[int, int]:
        """
        通用的图片尺寸获取方法
        支持多种图片格式
        """
        try:
            # 尝试导入torch，如果失败则使用模拟模式
            try:
                import torch
                torch_available = True
            except ImportError:
                torch_available = False
            
            # 处理PyTorch张量
            if torch_available and hasattr(image, 'shape') and str(type(image)).find('torch') != -1:
                if len(image.shape) == 4:  # [batch, height, width, channels]
                    height, width = image.shape[1], image.shape[2]
                elif len(image.shape) == 3:  # [height, width, channels]
                    height, width = image.shape[0], image.shape[1]
                else:
                    raise ValueError(f"不支持的张量形状: {image.shape}")
            else:
                # 处理其他格式 (包括Mock对象)
                if hasattr(image, 'shape'):
                    if len(image.shape) == 4:
                        height, width = image.shape[1], image.shape[2]
                    elif len(image.shape) == 3:
                        height, width = image.shape[0], image.shape[1]
                    else:
                        raise ValueError(f"不支持的数组形状: {image.shape}")
                elif hasattr(image, 'size'):
                    # PIL Image格式
                    width, height = image.size
                else:
                    raise ValueError("无法识别的图片格式")
            
            return int(width), int(height)
            
        except Exception as e:
            self.log_error(e, "获取图片尺寸")
            return 0, 0


class UtilityNode(PopoBaseNode):
    """
    实用工具节点的基础类
    为通用工具类节点提供基础功能
    """
    
    CATEGORY = "popo-utility/utils"


class TextProcessingNode(PopoBaseNode):
    """
    文本处理节点的基础类
    为文本处理相关的节点提供通用功能
    """
    
    CATEGORY = "popo-utility/text"


class MathNode(PopoBaseNode):
    """
    数学计算节点的基础类
    为数学计算相关的节点提供通用功能
    """
    
    CATEGORY = "popo-utility/math"