"""
ComfyUI Popo Utility - 自定义节点包初始化文件
使用模块化系统自动注册所有节点
"""

from .nodes import auto_register_nodes

# 自动发现并注册所有节点
NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = auto_register_nodes()

# 导出节点映射，供ComfyUI加载
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 版本信息
__version__ = "1.0.0"
__author__ = "Popo Utility Team"
__description__ = "ComfyUI图片处理实用工具集 - 模块化可扩展版本"

# ComfyUI会寻找这些变量来注册节点
WEB_DIRECTORY = "./web"  # 如果有前端文件的话

# 打印加载信息
print(f"🚀 Popo Utility v{__version__} 加载完成")
print(f"📦 已注册 {len(NODE_CLASS_MAPPINGS)} 个节点")

# 按类别显示节点信息
from .nodes import get_registry
registry = get_registry()
categories = registry.list_nodes_by_category()

for category, nodes in categories.items():
    print(f"📂 {category}: {len(nodes)} 个节点")
    for node in nodes:
        display_name = NODE_DISPLAY_NAME_MAPPINGS.get(node, node)
        print(f"   - {display_name}")