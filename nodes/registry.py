"""
ComfyUI Popo Utility - 节点注册系统
自动发现和注册所有节点类
"""

import importlib
import pkgutil
from typing import Dict, Any, List, Type, Optional
from .base_node import PopoBaseNode


class NodeRegistry:
    """
    节点注册系统
    自动发现并注册nodes包下的所有节点类
    """
    
    def __init__(self):
        self.node_classes: Dict[str, Type[PopoBaseNode]] = {}
        self.display_names: Dict[str, str] = {}
        self.categories: Dict[str, List[str]] = {}
        
    def discover_nodes(self) -> None:
        """
        自动发现nodes包下的所有节点
        """
        import sys
        import os
        
        # 获取当前nodes包的路径
        current_dir = os.path.dirname(__file__)
        
        # 遍历nodes包下的所有模块
        for importer, modname, ispkg in pkgutil.iter_modules([current_dir]):
            if modname.startswith('_') or modname == 'registry':
                continue  # 跳过私有模块和注册模块本身
                
            try:
                # 动态导入模块
                # 使用相对导入来避免冲突
                module = importlib.import_module(f".{modname}", package="nodes")
                
                # 查找模块中的NODE_CLASSES列表
                if hasattr(module, 'NODE_CLASSES'):
                    for node_class in module.NODE_CLASSES:
                        self._register_node_class(node_class)
                else:
                    # 如果没有NODE_CLASSES，尝试查找所有PopoBaseNode的子类
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, PopoBaseNode) and 
                            attr != PopoBaseNode and
                            not self._is_abstract_base_class(attr)):
                            self._register_node_class(attr)
                            
            except Exception as e:
                print(f"加载节点模块 {modname} 时出错: {e}")
    
    def _is_abstract_base_class(self, node_class: Type[PopoBaseNode]) -> bool:
        """
        判断是否为抽象基类（不应该注册到ComfyUI中）
        """
        # 基类名称列表（这些类不应该显示在ComfyUI中）
        base_class_names = {
            'PopoBaseNode',
            'ImageProcessingNode', 
            'UtilityNode',
            'TextProcessingNode',
            'MathNode'
        }
        
        class_name = node_class.__name__
        
        # 如果是基类名称列表中的类，则认为是抽象基类
        if class_name in base_class_names:
            return True
        
        # 检查是否没有实现必要的ComfyUI接口
        required_attrs = ['RETURN_TYPES', 'RETURN_NAMES', 'FUNCTION']
        for attr in required_attrs:
            if not hasattr(node_class, attr):
                return True
        
        return False
    
    def _register_node_class(self, node_class: Type[PopoBaseNode]) -> None:
        """
        注册单个节点类
        """
        try:
            class_name = node_class.__name__
            
            # 注册类
            self.node_classes[class_name] = node_class
            
            # 生成显示名称
            display_name = self._generate_display_name(class_name, node_class)
            self.display_names[class_name] = display_name
            
            # 按类别组织
            category = getattr(node_class, 'CATEGORY', 'popo-utility')
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(class_name)
            
            print(f"✅ 注册节点: {display_name} ({class_name})")
            
        except Exception as e:
            print(f"❌ 注册节点 {node_class.__name__} 时出错: {e}")
    
    def _generate_display_name(self, class_name: str, node_class: Type[PopoBaseNode]) -> str:
        """
        生成节点的显示名称
        """
        # 尝试从类中获取显示名称
        if hasattr(node_class, 'DISPLAY_NAME'):
            display_name_attr = getattr(node_class, 'DISPLAY_NAME', None)
            if display_name_attr:
                return str(display_name_attr)
        
        # 将驼峰命名转换为可读名称
        readable_name = self._camel_to_readable(class_name)
        
        return readable_name
    
    def _camel_to_readable(self, camel_str: str) -> str:
        """
        将驼峰命名转换为可读的名称
        """
        import re
        
        # 移除Node后缀
        if camel_str.endswith('Node'):
            camel_str = camel_str[:-4]
        
        # 在大写字母前添加空格
        result = re.sub(r'([A-Z])', r' \1', camel_str).strip()
        
        return result
    
    def get_comfyui_mappings(self) -> tuple:
        """
        获取ComfyUI需要的映射字典
        """
        return self.node_classes, self.display_names
    
    def get_node_info(self, class_name: str) -> Dict[str, Any]:
        """
        获取指定节点的详细信息
        """
        if class_name in self.node_classes:
            node_class = self.node_classes[class_name]
            instance = node_class()
            return instance.get_node_info()
        return {}
    
    def list_nodes_by_category(self) -> Dict[str, List[str]]:
        """
        按类别列出所有节点
        """
        return self.categories.copy()
    
    def register_manual_node(self, node_class: Type[PopoBaseNode], display_name: Optional[str] = None) -> None:
        """
        手动注册单个节点
        """
        class_name = node_class.__name__
        
        # 注册类
        self.node_classes[class_name] = node_class
        
        # 设置显示名称
        if display_name:
            self.display_names[class_name] = display_name
        else:
            self.display_names[class_name] = self._generate_display_name(class_name, node_class)
        
        # 按类别组织
        category = getattr(node_class, 'CATEGORY', 'popo-utility')
        if category not in self.categories:
            self.categories[category] = []
        if class_name not in self.categories[category]:
            self.categories[category].append(class_name)
        
        print(f"✅ 手动注册节点: {self.display_names[class_name]} ({class_name})")


# 全局注册器实例
registry = NodeRegistry()


def get_registry() -> NodeRegistry:
    """获取全局注册器实例"""
    return registry


def auto_register_nodes():
    """自动注册所有节点"""
    registry.discover_nodes()
    return registry.get_comfyui_mappings()