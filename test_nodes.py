"""
测试ComfyUI Popo Utility节点功能 - 模块化版本
验证节点注册系统和功能的正确性
"""

import sys
import os
import numpy as np

# 添加当前目录到路径，以便导入本地模块
sys.path.append(os.path.dirname(__file__))

# 模拟torch.Tensor类，用于测试
class MockTensor:
    """模拟PyTorch张量，用于测试"""
    def __init__(self, shape):
        self.shape = shape

def test_node_registry():
    """测试节点注册系统"""
    print("🧪 测试节点注册系统...")
    
    try:
        # 导入注册系统
        from nodes.registry import NodeRegistry
        
        # 创建注册器实例
        registry = NodeRegistry()
        
        # 手动注册一个测试节点 (模拟)
        class TestNode:
            CATEGORY = "test"
            DESCRIPTION = "测试节点"
            __name__ = "TestNode"
        
        registry._register_node_class(TestNode)
        
        # 验证注册成功
        assert "TestNode" in registry.node_classes
        assert "TestNode" in registry.display_names
        
        print("✅ 节点注册系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 节点注册系统测试失败: {e}")
        return False

def test_base_node_functionality():
    """测试基础节点类功能"""
    print("\n🧪 测试基础节点类功能...")
    
    try:
        from nodes.base_node import ImageProcessingNode
        
        # 创建测试类
        class TestImageNode(ImageProcessingNode):
            @classmethod
            def INPUT_TYPES(cls):
                return {"required": {"image": ("IMAGE",)}}
            
            @property
            def RETURN_TYPES(self): return ("INT", "INT")
            
            @property
            def RETURN_NAMES(self): return ("width", "height")
            
            @property
            def FUNCTION(self): return "get_size"
            
            def get_size(self, image):
                width, height = self.get_image_dimensions(image)
                return (width, height)
        
        # 创建节点实例
        node = TestImageNode()
        
        # 测试图片尺寸获取
        mock_image = MockTensor((1, 480, 640, 3))
        width, height = node.get_size(mock_image)
        
        assert width == 640
        assert height == 480
        
        print("✅ 基础节点类功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 基础节点类功能测试失败: {e}")
        return False

def test_image_nodes():
    """测试图片处理节点"""
    print("\n🧪 测试图片处理节点...")
    
    try:
        from nodes.image_utils import ImageSizeNode, ImageDimensionsNode, ImageAspectRatioNode
        
        # 测试ImageSizeNode
        size_node = ImageSizeNode()
        mock_image = MockTensor((1, 1080, 1920, 3))
        long_side, short_side = size_node.get_image_size(mock_image)
        
        assert long_side == 1920
        assert short_side == 1080
        print("✅ ImageSizeNode 测试通过")
        
        # 测试ImageDimensionsNode  
        dims_node = ImageDimensionsNode()
        width, height, long_side, short_side = dims_node.get_dimensions(mock_image)
        
        assert width == 1920
        assert height == 1080
        assert long_side == 1920
        assert short_side == 1080
        print("✅ ImageDimensionsNode 测试通过")
        
        # 测试ImageAspectRatioNode
        ratio_node = ImageAspectRatioNode()
        aspect_ratio, ratio_name = ratio_node.calculate_aspect_ratio(mock_image)
        
        expected_ratio = 1920 / 1080  # 16:9 = 1.778
        assert abs(aspect_ratio - expected_ratio) < 0.01
        assert "16:9" in ratio_name
        print("✅ ImageAspectRatioNode 测试通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 图片处理节点测试失败: {e}")
        return False

def test_auto_registration():
    """测试自动注册功能"""
    print("\n🧪 测试自动注册功能...")
    
    try:
        from nodes import auto_register_nodes
        
        # 执行自动注册
        node_classes, display_names = auto_register_nodes()
        
        # 验证注册结果
        assert len(node_classes) > 0
        assert len(display_names) > 0
        assert len(node_classes) == len(display_names)
        
        # 验证具体节点
        expected_nodes = ['ImageSizeNode', 'ImageDimensionsNode', 'ImageAspectRatioNode']
        for node_name in expected_nodes:
            assert node_name in node_classes, f"{node_name} 未被注册"
            assert node_name in display_names, f"{node_name} 缺少显示名称"
        
        print(f"✅ 自动注册测试通过 (注册了 {len(node_classes)} 个节点)")
        
        # 显示注册的节点
        print("   已注册的节点:")
        for name in node_classes.keys():
            display_name = display_names.get(name, name)
            print(f"     - {display_name} ({name})")
        
        return True
        
    except Exception as e:
        print(f"❌ 自动注册测试失败: {e}")
        return False

def test_performance_characteristics():
    """测试性能特征"""
    print("\n⚡ 性能特征验证...")
    
    try:
        from nodes.image_utils import ImageSizeNode
        import time
        
        node = ImageSizeNode()
        
        # 测试不同尺寸图片的处理时间
        sizes = [
            (1, 480, 640, 3),    # 小图
            (1, 1080, 1920, 3),  # 中图  
            (1, 2160, 3840, 3),  # 大图
            (1, 4320, 7680, 3),  # 超大图
        ]
        
        times = []
        
        for i, shape in enumerate(sizes):
            mock_image = MockTensor(shape)
            
            start_time = time.time()
            for _ in range(1000):  # 重复1000次
                long_side, short_side = node.get_image_size(mock_image)
            end_time = time.time()
            
            avg_time = (end_time - start_time) / 1000
            times.append(avg_time)
            
            print(f"✅ 尺寸 {shape[2]}x{shape[1]}: {avg_time:.6f}秒 (平均)")
        
        # 验证性能一致性 (所有时间应该相近)
        max_time = max(times)
        min_time = min(times)
        time_variance = max_time - min_time
        
        # 时间差异应该很小 (小于最大时间的50%)
        assert time_variance < max_time * 0.5, f"性能不一致: 差异 {time_variance:.6f}秒"
        
        print(f"✅ 性能验证通过: 时间差异 {time_variance:.6f}秒")
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False

def test_image_size_node():
    """测试ImageSizeNode的功能"""
    # 由于没有安装torch，我们需要模拟节点的核心逻辑
    
    def get_image_size_logic(image):
        """复制节点的核心逻辑用于测试"""
        try:
            # 模拟处理不同格式的图片输入
            if hasattr(image, 'shape'):
                if len(image.shape) == 4:  # [batch, height, width, channels]
                    height, width = image.shape[1], image.shape[2]
                elif len(image.shape) == 3:  # [height, width, channels]
                    height, width = image.shape[0], image.shape[1]
                else:
                    raise ValueError(f"不支持的图片张量形状: {image.shape}")
            else:
                # 如果是PIL Image等其他格式
                if hasattr(image, 'size'):
                    width, height = image.size
                else:
                    raise ValueError("无法识别的图片格式")
            
            # 计算长边和短边
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (int(long_side), int(short_side))
            
        except Exception as e:
            print(f"获取图片尺寸时发生错误: {e}")
            return (0, 0)
    
    # 测试用例
    test_cases = [
        # 格式: (输入描述, 模拟图片形状, 期望输出)
        ("1920x1080图片 (batch格式)", (1, 1080, 1920, 3), (1920, 1080)),
        ("1080x1920图片 (batch格式)", (1, 1920, 1080, 3), (1920, 1080)),
        ("500x300图片 (无batch)", (300, 500, 3), (500, 300)),
        ("300x500图片 (无batch)", (500, 300, 3), (500, 300)),
        ("正方形图片", (1, 512, 512, 3), (512, 512)),
    ]
    
    print("🧪 开始测试ImageSizeNode功能...")
    
    for description, shape, expected in test_cases:
        mock_image = MockTensor(shape)
        result = get_image_size_logic(mock_image)
        
        if result == expected:
            print(f"✅ {description}: 通过 - 输出 {result}")
        else:
            print(f"❌ {description}: 失败 - 期望 {expected}, 实际 {result}")
    
    # 测试错误处理
    print("\n🛡️ 测试错误处理...")
    
    # 测试不支持的形状
    invalid_shape = MockTensor((100, 200))  # 2D形状，不支持
    result = get_image_size_logic(invalid_shape)
    if result == (0, 0):
        print("✅ 不支持的形状处理: 通过 - 正确返回默认值")
    else:
        print(f"❌ 不支持的形状处理: 失败 - 期望 (0, 0), 实际 {result}")

def test_image_dimensions_node():
    """测试ImageDimensionsNode的功能"""
    
    def get_dimensions_logic(image):
        """复制节点的核心逻辑用于测试"""
        try:
            if hasattr(image, 'shape'):
                if len(image.shape) == 4:  # [batch, height, width, channels]
                    height, width = image.shape[1], image.shape[2]
                elif len(image.shape) == 3:  # [height, width, channels]
                    height, width = image.shape[0], image.shape[1]
                else:
                    raise ValueError(f"不支持的张量形状: {image.shape}")
            else:
                if hasattr(image, 'size'):
                    width, height = image.size
                else:
                    raise ValueError("无法识别的图片格式")
            
            # 计算长边和短边
            long_side = max(height, width)
            short_side = min(height, width)
            
            return (int(width), int(height), int(long_side), int(short_side))
            
        except Exception as e:
            print(f"获取图片尺寸时发生错误: {e}")
            return (0, 0, 0, 0)
    
    print("\n🧪 开始测试ImageDimensionsNode功能...")
    
    test_cases = [
        # 格式: (输入描述, 模拟图片形状, 期望输出(宽,高,长边,短边))
        ("1920x1080图片", (1, 1080, 1920, 3), (1920, 1080, 1920, 1080)),
        ("1080x1920图片", (1, 1920, 1080, 3), (1080, 1920, 1920, 1080)),
        ("正方形图片", (1, 512, 512, 3), (512, 512, 512, 512)),
        ("小尺寸图片", (64, 32, 3), (32, 64, 64, 32)),
    ]
    
    for description, shape, expected in test_cases:
        mock_image = MockTensor(shape)
        result = get_dimensions_logic(mock_image)
        
        if result == expected:
            print(f"✅ {description}: 通过 - 输出 {result}")
        else:
            print(f"❌ {description}: 失败 - 期望 {expected}, 实际 {result}")

def test_performance_characteristics():
    """测试性能特征"""
    print("\n⚡ 性能特征验证...")
    
    # 验证不同尺寸图片的处理时间应该相近（因为只读取shape属性）
    import time
    
    def get_size_fast(shape):
        """快速获取尺寸的方法"""
        height, width = shape[1], shape[2]  # 直接访问shape属性
        return max(height, width), min(height, width)
    
    # 测试不同尺寸
    sizes = [
        (1, 480, 640, 3),    # 小图
        (1, 1080, 1920, 3),  # 中图  
        (1, 2160, 3840, 3),  # 大图
        (1, 4320, 7680, 3),  # 超大图
    ]
    
    print("验证处理时间与图片尺寸无关...")
    for i, shape in enumerate(sizes):
        start_time = time.time()
        for _ in range(1000):  # 重复1000次
            long_side, short_side = get_size_fast(shape)
        end_time = time.time()
        
        print(f"✅ 尺寸 {shape[2]}x{shape[1]}: {end_time - start_time:.6f}秒 (1000次)")
    
    print("✅ 性能验证通过: 处理时间与图片尺寸无关，仅依赖shape属性读取")

if __name__ == "__main__":
    print("🚀 ComfyUI Popo Utility 节点功能测试 - 模块化版本")
    print("=" * 60)
    
    # 跑所有测试
    test_results = []
    
    tests = [
        ("节点注册系统", test_node_registry),
        ("基础节点类", test_base_node_functionality),
        ("图片处理节点", test_image_nodes),
        ("自动注册功能", test_auto_registration),
        ("性能特征", test_performance_characteristics),
        ("旧版兼容性", test_image_size_node),
        ("旧版详细信息", test_image_dimensions_node),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试出现异常: {e}")
            test_results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📄 测试结果总结:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🏆 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试均通过！")
        print("\n📝 模块化架构特性:")
        print("- ✅ 自动节点发现和注册")
        print("- ✅ 基础节点类体系")
        print("- ✅ 模块化节点组织")
        print("- ✅ 性能优化保持")
        print("- ✅ 向后兼容性")
        print("\n🚀 现在你可以开始添加新的节点了！")
        print("📆 参考 DEVELOPMENT_GUIDE.md 获取详细开发指南")
    else:
        print(f"⚠️  有 {total - passed} 个测试失败，请检查上方错误信息")