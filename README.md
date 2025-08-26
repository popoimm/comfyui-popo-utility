# ComfyUI Popo Utility

🚀 **高性能的ComfyUI自定义节点工具集** - 🔧 **模块化可扩展架构**

一个专为ComfyUI设计的图片处理实用工具集，采用模块化架构设计，支持快速扩展和添加新节点。

## ⭐ 核心特性

### 🏗️ 模块化架构
- 📦 **自动节点发现** - 新节点自动注册，无需手动配置
- 🔧 **扩展友好** - 基于模板的节点开发，5分钟创建新节点  
- 📂 **分类管理** - 节点按功能自动分类组织
- 🎯 **插件化设计** - 支持独立开发和部署节点模块

### ⚡ 性能优化
- 🚀 **零拷贝设计** - 直接从张量shape获取信息，避免数据转换
- ⏱️ **常数时间复杂度** - 处理时间与图片大小无关
- 🧠 **内存友好** - 最小化内存占用，高效处理大图片
- 🛡️ **稳定可靠** - 完善的错误处理，避免节点崩溃

## 📦 安装方法

### 方法一：直接安装到ComfyUI

1. 将本项目克隆到ComfyUI的自定义节点目录：
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/your-username/comfyui-popo-utility.git
```

2. 重启ComfyUI即可使用

### 方法二：手动安装

1. 下载本项目的所有文件
2. 将文件夹复制到 `ComfyUI/custom_nodes/` 目录下
3. 重启ComfyUI

## 🎯 节点说明

### 🖼️ 图片长短边尺寸 (ImageSizeNode)

**功能**：获取图片的长边和短边尺寸

**输入**：
- `image` - 图片输入（IMAGE类型）

**输出**：
- `long_side` - 长边尺寸（INT类型）
- `short_side` - 短边尺寸（INT类型）

**使用场景**：
- 需要根据图片尺寸进行条件判断
- 图片缩放比例计算
- 画面比例分析

### 📏 图片详细尺寸 (ImageDimensionsNode)

**功能**：获取图片的详细尺寸信息

**输入**：
- `image` - 图片输入（IMAGE类型）

**输出**：
- `width` - 宽度（INT类型）
- `height` - 高度（INT类型）  
- `long_side` - 长边尺寸（INT类型）
- `short_side` - 短边尺寸（INT类型）

**使用场景**：
- 需要完整的图片尺寸信息
- 图片布局计算
- 分辨率分析

## 🚀 性能优化

本工具集在性能方面做了以下优化：

1. **直接张量操作** - 直接从PyTorch张量的形状属性获取尺寸，避免图片格式转换
2. **零拷贝设计** - 不对原始图片数据进行任何修改或复制
3. **快速失败机制** - 完善的错误处理，遇到异常时快速返回默认值
4. **内存友好** - 不存储额外的图片数据，内存占用极小

## 🔧 模块化架构

项目采用模块化设计，为未来扩展做好了准备：

### 📁 项目结构
```
comfyui-popo-utility/
├── __init__.py              # 主入口，自动注册所有节点
├── nodes/                   # 节点包目录
│   ├── __init__.py         # 节点包初始化
│   ├── base_node.py        # 基础节点类
│   ├── registry.py         # 自动注册系统
│   ├── image_utils.py      # 图片处理节点
│   └── [your_nodes].py     # 您的自定义节点
├── node_template.py         # 新节点开发模板  
├── DEVELOPMENT_GUIDE.md     # 详细开发指南
└── README.md               # 项目说明
```

### 🎯 快速添加新节点

只需要 **3步** 就能添加新节点：

```bash
# 1. 复制模板
cp node_template.py nodes/my_new_nodes.py

# 2. 编辑新文件，实现你的节点功能
# 3. 重启ComfyUI，节点会自动被注册🎉
```

### 📄 基础类体系

| 基础类 | 用途 | 分类 |
|--------|------|------|
| `PopoBaseNode` | 通用节点基类 | `popo-utility` |
| `ImageProcessingNode` | 图片处理相关 | `popo-utility/image` |
| `TextProcessingNode` | 文本处理相关 | `popo-utility/text` |
| `MathNode` | 数学计算相关 | `popo-utility/math` |
| `UtilityNode` | 实用工具相关 | `popo-utility/utils` |

### 📝 新节点开发示例

```python
# 在 nodes/my_nodes.py 中
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

更多详细内容请参考 📚 [**开发指南**](DEVELOPMENT_GUIDE.md)

## 📝 使用示例

### 基础工作流

```
[Load Image] → [图片长短边尺寸] → [输出长边和短边]
                     ↓
                [其他处理节点]
```

### 高级工作流

```
[Load Image] → [图片详细尺寸] → [条件判断节点]
                     ↓              ↓
                [宽度/高度]    [长边/短边]
                     ↓              ↓
                [不同的处理分支]
```

## 🔧 技术细节

- **兼容性**：支持ComfyUI标准的图片张量格式
- **输入格式**：[batch, height, width, channels] 或 [height, width, channels]
- **数据类型**：支持PyTorch Tensor、NumPy Array、PIL Image
- **Python版本**：>=3.8
- **依赖项**：PyTorch, NumPy, Pillow

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 支持与反馈

如果您在使用过程中遇到任何问题或有改进建议，请：

- 提交 [GitHub Issues](https://github.com/your-username/comfyui-popo-utility/issues)
- 参与 [GitHub Discussions](https://github.com/your-username/comfyui-popo-utility/discussions)

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！** ⭐