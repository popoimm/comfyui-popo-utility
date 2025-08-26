# 🚀 ComfyUI Popo Utility 节点开发指南

本指南将帮助您快速开发和添加新的ComfyUI自定义节点到Popo Utility工具集中。

## 📋 目录

- [快速开始](#快速开始)
- [项目结构](#项目结构) 
- [节点开发流程](#节点开发流程)
- [基础类介绍](#基础类介绍)
- [开发最佳实践](#开发最佳实践)
- [测试指南](#测试指南)
- [常见问题](#常见问题)

## 🚀 快速开始

### 1. 使用模板创建新节点

```bash
# 1. 复制模板文件
cp node_template.py nodes/my_new_nodes.py

# 2. 编辑新文件，实现您的节点功能
# 3. 重启ComfyUI，节点会自动被注册
```

### 2. 最简单的节点示例

```python
from nodes.base_node import UtilityNode

class HelloWorldNode(UtilityNode):
    DESCRIPTION = "简单的Hello World节点"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "World"}),
            }
        }
    
    @property 
    def RETURN_TYPES(self): return ("STRING",)
    
    @property
    def RETURN_NAMES(self): return ("greeting",)
    
    @property 
    def FUNCTION(self): return "say_hello"
    
    def say_hello(self, name: str):
        return (f"Hello, {name}!",)

# 记得添加到NODE_CLASSES列表
NODE_CLASSES = [HelloWorldNode]
```

## 📁 项目结构

```
comfyui-popo-utility/
├── __init__.py                 # 主入口，自动注册所有节点
├── nodes/                      # 节点包目录
│   ├── __init__.py            # 节点包初始化
│   ├── base_node.py           # 基础节点类
│   ├── registry.py            # 自动注册系统
│   ├── image_utils.py         # 图片处理节点
│   └── [your_nodes].py        # 您的自定义节点
├── node_template.py           # 新节点开发模板
├── DEVELOPMENT_GUIDE.md       # 本开发指南
└── test_nodes.py             # 节点测试
```

## 🔄 节点开发流程

### Step 1: 选择合适的基础类

| 基础类 | 用途 | 分类 |
|--------|------|------|
| `PopoBaseNode` | 通用节点基类 | `popo-utility` |
| `ImageProcessingNode` | 图片处理相关 | `popo-utility/image` |
| `TextProcessingNode` | 文本处理相关 | `popo-utility/text` |
| `MathNode` | 数学计算相关 | `popo-utility/math` |
| `UtilityNode` | 实用工具相关 | `popo-utility/utils` |

### Step 2: 实现必需的方法和属性

```python
class MyNode(PopoBaseNode):
    # 必需实现的方法和属性
    
    @classmethod
    def INPUT_TYPES(cls):
        # 定义输入类型
        return {"required": {...}}
    
    @property
    def RETURN_TYPES(self):
        # 定义返回类型
        return ("TYPE1", "TYPE2")
    
    @property  
    def RETURN_NAMES(self):
        # 定义返回名称
        return ("name1", "name2")
    
    @property
    def FUNCTION(self):
        # 定义执行函数名
        return "my_function"
    
    def my_function(self, **kwargs):
        # 主要逻辑实现
        return (result1, result2)
```

### Step 3: 添加到NODE_CLASSES列表

```python
# 文件末尾
NODE_CLASSES = [
    MyNode,
    AnotherNode,
    # 添加更多节点...
]
```

### Step 4: 测试和验证

```python
# 运行测试
python test_nodes.py

# 或创建专门的测试
def test_my_node():
    node = MyNode()
    result = node.my_function(input1="test")
    assert result[0] == expected_value
```

## 🧩 基础类介绍

### PopoBaseNode

所有节点的基础类，提供：

- 统一的错误处理: `self.log_error()`
- 输入验证: `self.validate_inputs()`
- 节点信息获取: `self.get_node_info()`

### ImageProcessingNode

图片处理节点基类，额外提供：

- 图片尺寸获取: `self.get_image_dimensions(image)`
- 支持多种图片格式 (Tensor, Array, PIL)
- 自动错误处理和默认值返回

使用示例：

```python
class MyImageNode(ImageProcessingNode):
    def process_image(self, image):
        width, height = self.get_image_dimensions(image)
        # 使用width和height进行处理...
        return (width, height)
```

## 💡 开发最佳实践

### 1. 命名规范

- **类名**: PascalCase + Node后缀 (如: `ImageResizeNode`)
- **文件名**: snake_case (如: `image_utils.py`)  
- **函数名**: snake_case (如: `process_image`)
- **变量名**: snake_case (如: `image_width`)

### 2. 错误处理

```python
def my_function(self, input_data):
    try:
        # 输入验证
        if not self.validate_inputs(input_data=input_data):
            return self._get_default_return()
        
        # 主要逻辑
        result = process_data(input_data)
        return (result,)
        
    except Exception as e:
        self.log_error(e, "my_function")
        return self._get_default_return()

def _get_default_return(self):
    """返回默认值，避免节点崩溃"""
    return (0,)  # 根据RETURN_TYPES调整
```

### 3. 输入类型配置

```python
@classmethod
def INPUT_TYPES(cls):
    return {
        "required": {
            # 数字输入
            "number": ("INT", {
                "default": 1,
                "min": 0,
                "max": 100,
                "step": 1,
            }),
            
            # 浮点数输入  
            "ratio": ("FLOAT", {
                "default": 1.0,
                "min": 0.0,
                "max": 10.0,
                "step": 0.1,
            }),
            
            # 字符串输入
            "text": ("STRING", {
                "default": "默认文本",
                "multiline": False,
            }),
            
            # 选择列表
            "mode": (["mode1", "mode2", "mode3"], {
                "default": "mode1"
            }),
            
            # 布尔值
            "enable": ("BOOLEAN", {
                "default": True
            }),
        },
        "optional": {
            # 可选输入...
        }
    }
```

### 4. 性能优化

```python
def process_large_data(self, data):
    # ✅ 好的做法：使用numpy操作
    import numpy as np
    result = np.array(data) * 2
    
    # ❌ 避免：Python循环处理大数据
    # result = [x * 2 for x in data]
    
    return (result.tolist(),)

def get_image_info(self, image):
    # ✅ 好的做法：直接从shape获取信息
    if hasattr(image, 'shape'):
        height, width = image.shape[:2]
    
    # ❌ 避免：转换图片格式后再获取信息
    # pil_image = tensor_to_pil(image)
    # width, height = pil_image.size
    
    return (width, height)
```

## 🧪 测试指南

### 1. 单元测试结构

```python
def test_my_node():
    """测试MyNode的基本功能"""
    
    # 创建节点实例
    node = MyNode()
    
    # 准备测试数据
    test_input = "test_data"
    
    # 执行测试
    result = node.my_function(test_input)
    
    # 验证结果
    assert len(result) == 2  # 检查返回值数量
    assert result[0] == expected_value_1
    assert result[1] == expected_value_2
    
    print("✅ MyNode基本功能测试通过")

def test_my_node_error_handling():
    """测试MyNode的错误处理"""
    
    node = MyNode()
    
    # 测试无效输入
    result = node.my_function(None)
    assert result == (0, "")  # 默认值
    
    print("✅ MyNode错误处理测试通过")
```

### 2. 性能测试

```python
import time

def test_node_performance():
    """测试节点性能"""
    
    node = MyNode()
    test_data = generate_large_test_data()
    
    start_time = time.time()
    for _ in range(100):
        result = node.my_function(test_data)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 100
    print(f"平均处理时间: {avg_time:.6f}秒")
    
    # 性能要求检查
    assert avg_time < 0.01  # 要求小于10ms
```

### 3. 集成测试

```python
def test_node_integration():
    """测试节点集成"""
    
    # 模拟ComfyUI工作流
    from nodes.registry import get_registry
    
    registry = get_registry()
    node_classes, display_names = registry.get_comfyui_mappings()
    
    # 验证节点已注册
    assert "MyNode" in node_classes
    assert "MyNode" in display_names
    
    print("✅ 节点集成测试通过")
```

## ❓ 常见问题

### Q1: 如何调试节点？

```python
def my_function(self, input_data):
    # 添加调试输出
    print(f"[DEBUG] 输入数据: {input_data}")
    print(f"[DEBUG] 数据类型: {type(input_data)}")
    
    # 使用断言检查中间结果
    processed = process_data(input_data)
    assert processed is not None, "处理结果不能为空"
    
    return (processed,)
```

### Q2: 节点没有出现在ComfyUI中？

1. 检查NODE_CLASSES列表是否包含您的节点
2. 确认节点类继承自正确的基础类
3. 查看ComfyUI控制台的错误信息
4. 重启ComfyUI

### Q3: 如何处理复杂的输入验证？

```python
def validate_inputs(self, **kwargs):
    """自定义输入验证"""
    
    # 调用基类验证
    if not super().validate_inputs(**kwargs):
        return False
    
    # 自定义验证逻辑
    image = kwargs.get('image')
    if image is not None:
        width, height = self.get_image_dimensions(image)
        if width < 32 or height < 32:
            print("图片尺寸太小，最小32x32")
            return False
    
    threshold = kwargs.get('threshold', 0)
    if not 0 <= threshold <= 1:
        print("阈值必须在0-1之间")  
        return False
    
    return True
```

### Q4: 如何优化内存使用？

```python
def process_image(self, image):
    # ✅ 直接在原始张量上操作
    if hasattr(image, 'shape'):
        # 只读取需要的信息
        height, width = image.shape[1:3]
    
    # ❌ 避免创建不必要的副本
    # image_copy = image.clone()  # 占用额外内存
    
    return (width, height)
```

## 🎯 高级特性

### 自定义显示名称和分类

```python
class MyAdvancedNode(PopoBaseNode):
    DISPLAY_NAME = "🎨 我的高级节点"  # 自定义显示名称
    CATEGORY = "popo-utility/advanced"  # 自定义分类
    DESCRIPTION = "这是一个高级功能节点"
```

### 条件输入

```python
@classmethod
def INPUT_TYPES(cls):
    return {
        "required": {
            "mode": (["simple", "advanced"],)
        },
        "optional": {
            # 只在advanced模式下显示
            "advanced_param": ("FLOAT", {
                "default": 1.0,
                # 可以添加显示条件逻辑
            }),
        }
    }
```

---

💡 **提示**: 开发过程中遇到问题，可以查看现有节点的实现作为参考，或者在项目的GitHub Issues中提问。

🚀 **开始开发您的第一个节点吧！**