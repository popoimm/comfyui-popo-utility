#!/usr/bin/env python3
"""
ComfyUI 特定格式测试
模拟ComfyUI的精确加载过程
"""

import sys
import os

def test_comfyui_loading():
    """模拟ComfyUI的节点加载过程"""
    
    print("🔍 ComfyUI 特定格式测试")
    print("=" * 40)
    
    # 模拟ComfyUI的导入方式
    try:
        # 这是ComfyUI实际使用的导入方式
        spec = None
        try:
            import importlib.util
            file_path = os.path.join(os.getcwd(), "__init__.py")
            spec = importlib.util.spec_from_file_location("comfyui_popo_utility", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"❌ 模块加载失败: {e}")
            return False
        
        # 检查必需的属性
        if not hasattr(module, 'NODE_CLASS_MAPPINGS'):
            print("❌ 缺少 NODE_CLASS_MAPPINGS")
            return False
            
        if not hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
            print("❌ 缺少 NODE_DISPLAY_NAME_MAPPINGS")
            return False
        
        mappings = module.NODE_CLASS_MAPPINGS
        display_mappings = module.NODE_DISPLAY_NAME_MAPPINGS
        
        print(f"✅ 成功加载 {len(mappings)} 个节点")
        
        # 检查每个节点的ComfyUI兼容性
        for class_name, node_class in mappings.items():
            print(f"\n🔍 检查节点: {class_name}")
            
            # 检查必需的ComfyUI属性
            required_attrs = ['INPUT_TYPES', 'RETURN_TYPES', 'RETURN_NAMES', 'FUNCTION', 'CATEGORY']
            missing_attrs = []
            
            for attr in required_attrs:
                if not hasattr(node_class, attr):
                    missing_attrs.append(attr)
            
            if missing_attrs:
                print(f"   ❌ 缺少属性: {missing_attrs}")
                continue
            
            # 检查INPUT_TYPES是否可调用
            if not callable(node_class.INPUT_TYPES):
                print(f"   ❌ INPUT_TYPES不是可调用方法")
                continue
            
            # 测试INPUT_TYPES调用
            try:
                input_types = node_class.INPUT_TYPES()
                if not isinstance(input_types, dict) or 'required' not in input_types:
                    print(f"   ❌ INPUT_TYPES格式错误")
                    continue
                print(f"   ✅ INPUT_TYPES: 格式正确")
            except Exception as e:
                print(f"   ❌ INPUT_TYPES调用失败: {e}")
                continue
            
            # 检查其他属性类型
            if not isinstance(node_class.RETURN_TYPES, tuple):
                print(f"   ❌ RETURN_TYPES不是元组")
                continue
            
            if not isinstance(node_class.RETURN_NAMES, tuple):
                print(f"   ❌ RETURN_NAMES不是元组")
                continue
                
            if not isinstance(node_class.FUNCTION, str):
                print(f"   ❌ FUNCTION不是字符串")
                continue
                
            if not isinstance(node_class.CATEGORY, str):
                print(f"   ❌ CATEGORY不是字符串")
                continue
            
            # 测试节点实例化
            try:
                instance = node_class()
                func_name = node_class.FUNCTION
                if not hasattr(instance, func_name):
                    print(f"   ❌ 缺少执行函数: {func_name}")
                    continue
                print(f"   ✅ 执行函数 '{func_name}' 存在")
            except Exception as e:
                print(f"   ❌ 实例化失败: {e}")
                continue
            
            # 显示节点信息
            display_name = display_mappings.get(class_name, class_name)
            category = node_class.CATEGORY
            print(f"   ✅ 显示名称: {display_name}")
            print(f"   ✅ 类别: {category}")
            print(f"   ✅ 所有检查通过")
        
        print("\n" + "=" * 40)
        print("🎉 ComfyUI兼容性测试完成!")
        
        # 生成ComfyUI使用说明
        print("\n📋 在ComfyUI中查找节点:")
        for class_name, node_class in mappings.items():
            display_name = display_mappings.get(class_name, class_name)
            category = node_class.CATEGORY
            print(f"   右键 → Add Node → {category} → {display_name}")
        
        print("\n🔍 搜索关键词:")
        search_terms = set()
        for display_name in display_mappings.values():
            words = display_name.replace("Popo ", "").split()
            search_terms.update(words)
        print(f"   {', '.join(sorted(search_terms))}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_comfyui_loading()
    if success:
        print("\n✅ 节点应该能在ComfyUI中正常显示!")
    else:
        print("\n❌ 存在兼容性问题，需要修复!")
    
    sys.exit(0 if success else 1)