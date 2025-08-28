"""
ComfyUI Popo Utility - 简化版直接导入
这是一个完全兼容ComfyUI的简化版本
"""

# 直接导入节点类
try:
    from .nodes_direct import (
        PopoImageSizeNode,
        PopoImageDimensionsNode, 
        PopoImageAspectRatioNode,
        PopoMathExpressionNode
    )
except ImportError:
    from nodes_direct import (
        PopoImageSizeNode,
        PopoImageDimensionsNode, 
        PopoImageAspectRatioNode,
        PopoMathExpressionNode
    )

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

# 版本信息
__version__ = "1.0.1"

# 简化的加载信息
print(f"Popo Utility v{__version__} - Simple version loaded!")
print(f"Nodes: {list(NODE_DISPLAY_NAME_MAPPINGS.values())}")

# 导出给ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']