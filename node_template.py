"""
ComfyUI Popo Utility - 新节点开发模板
复制此文件并根据需要修改来创建新节点

使用步骤:
1. 复制此模板文件到 nodes/ 目录下
2. 重命名为合适的文件名 (如: text_utils.py, math_utils.py 等)
3. 修改类名、功能实现和配置
4. 在文件末尾的 NODE_CLASSES 列表中添加新的节点类
5. 重启ComfyUI，新节点会自动被发现和注册
"""

from nodes.base_node import PopoBaseNode, ImageProcessingNode, UtilityNode, TextProcessingNode, MathNode
from typing import Tuple, Dict, Any


class TemplateNode(PopoBaseNode):
    """
    模板节点类 - 继承自PopoBaseNode
    
    选择合适的基础类:
    - PopoBaseNode: 通用节点基类
    - ImageProcessingNode: 图片处理节点  
    - UtilityNode: 实用工具节点
    - TextProcessingNode: 文本处理节点
    - MathNode: 数学计算节点
    """
    
    # 节点描述信息
    DESCRIPTION = "这是一个模板节点，请修改为实际功能描述"
    
    # 可选: 自定义显示名称
    # DISPLAY_NAME = "🔧 模板节点"
    
    # 可选: 自定义分类 (如果不设置，会使用基础类的分类)
    # CATEGORY = "popo-utility/custom"
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """
        定义节点的输入类型
        
        常用输入类型:
        - "IMAGE": 图片输入
        - "STRING": 字符串输入
        - "INT": 整数输入  
        - "FLOAT": 浮点数输入
        - "BOOLEAN": 布尔值输入
        """
        return {
            "required": {
                # 必需的输入
                "input_value": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }),
            },
            "optional": {
                # 可选的输入
                "optional_text": ("STRING", {
                    "default": "默认文本",
                }),
            }
        }
    
    @property
    def RETURN_TYPES(self) -> Tuple:
        """
        定义节点的返回类型
        
        常用返回类型:
        - "INT": 整数
        - "FLOAT": 浮点数  
        - "STRING": 字符串
        - "IMAGE": 图片
        - "BOOLEAN": 布尔值
        """
        return ("INT", "STRING")
    
    @property
    def RETURN_NAMES(self) -> Tuple:
        """定义返回值的名称"""
        return ("result_number", "result_text")
    
    @property
    def FUNCTION(self) -> str:
        """定义执行函数的名称"""
        return "process"
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        输入验证 (可选重写)
        """
        # 添加自定义验证逻辑
        return super().validate_inputs(**kwargs)
    
    def process(self, input_value: int, optional_text: str = "默认文本"):
        """
        节点的主要处理函数
        
        Args:
            input_value: 输入的整数值
            optional_text: 可选的文本输入
        
        Returns:
            tuple: 返回处理结果
        """
        try:
            # 输入验证
            if not self.validate_inputs(input_value=input_value, optional_text=optional_text):
                return (0, "验证失败")
            
            # 主要处理逻辑
            result_number = input_value * 2  # 示例: 将输入值乘以2
            result_text = f"处理结果: {result_number}, 文本: {optional_text}"
            
            return (result_number, result_text)
            
        except Exception as e:
            self.log_error(e, "process")
            return (0, f"错误: {str(e)}")


class AdvancedTemplateNode(ImageProcessingNode):
    """
    高级模板节点 - 继承自ImageProcessingNode
    展示如何使用基类提供的图片处理功能
    """
    
    DESCRIPTION = "高级模板节点，展示图片处理功能"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "scale_factor": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1,
                }),
            }
        }
    
    @property
    def RETURN_TYPES(self) -> Tuple:
        return ("INT", "INT", "STRING")
    
    @property
    def RETURN_NAMES(self) -> Tuple:
        return ("scaled_width", "scaled_height", "info")
    
    @property
    def FUNCTION(self) -> str:
        return "process_image"
    
    def process_image(self, image, scale_factor: float):
        """
        图片处理示例函数
        """
        try:
            # 使用基类的图片尺寸获取功能
            width, height = self.get_image_dimensions(image)
            
            if width == 0 or height == 0:
                return (0, 0, "无效图片")
            
            # 计算缩放后的尺寸
            scaled_width = int(width * scale_factor)
            scaled_height = int(height * scale_factor)
            
            info = f"原尺寸: {width}x{height}, 缩放后: {scaled_width}x{scaled_height}"
            
            return (scaled_width, scaled_height, info)
            
        except Exception as e:
            self.log_error(e, "process_image")
            return (0, 0, f"处理错误: {str(e)}")


# ================================
# 重要: 在这里添加所有要注册的节点类
# ================================
NODE_CLASSES = [
    TemplateNode,
    AdvancedTemplateNode,
    # 在这里添加更多节点类...
]

# ================================
# 开发提示
# ================================
"""
节点开发最佳实践:

1. 命名规范:
   - 节点类名使用 PascalCase，以 Node 结尾
   - 文件名使用 snake_case
   - 函数名使用 snake_case

2. 错误处理:
   - 总是使用 try-except 包装主要逻辑
   - 使用 self.log_error() 记录错误
   - 返回合理的默认值而不是抛出异常

3. 输入验证:
   - 重写 validate_inputs() 方法添加自定义验证
   - 检查输入范围和类型
   - 提供有意义的错误信息

4. 性能优化:
   - 避免不必要的数据复制
   - 使用numpy操作而非Python循环
   - 缓存计算结果(如果适用)

5. 文档编写:
   - 为每个节点添加详细的docstring
   - 说明输入输出参数的含义
   - 提供使用示例

6. 测试:
   - 为每个节点编写单元测试
   - 测试边界条件和错误情况
   - 验证性能要求
"""