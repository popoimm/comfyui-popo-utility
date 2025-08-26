"""
ComfyUI Popo Utility - Nodes Package
节点包初始化文件
"""

from .base_node import (
    PopoBaseNode,
    ImageProcessingNode, 
    UtilityNode,
    TextProcessingNode,
    MathNode
)

from .registry import (
    NodeRegistry,
    get_registry,
    auto_register_nodes
)

# 导入所有节点模块以确保它们被注册
from . import image_utils

__all__ = [
    # 基础类
    'PopoBaseNode',
    'ImageProcessingNode',
    'UtilityNode', 
    'TextProcessingNode',
    'MathNode',
    
    # 注册系统
    'NodeRegistry',
    'get_registry',
    'auto_register_nodes',
]