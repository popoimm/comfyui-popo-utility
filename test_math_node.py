#!/usr/bin/env python3
"""
数学表达式节点测试
测试PopoMathExpressionNode的功能
"""

import sys
import os
import math
import unittest
from unittest.mock import MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 模拟ComfyUI环境
sys.modules['torch'] = MagicMock()
sys.modules['numpy'] = MagicMock()

from nodes_direct import PopoMathExpressionNode


class TestPopoMathExpressionNode(unittest.TestCase):
    """数学表达式节点测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.node = PopoMathExpressionNode()
    
    def test_basic_arithmetic(self):
        """测试基础算术运算"""
        # 加法
        result_int, result_float = self.node.calculate_expression(10, 5, 3, "a + b + c")
        self.assertEqual(result_int, 18)
        self.assertEqual(result_float, 18.0)
        
        # 减法
        result_int, result_float = self.node.calculate_expression(10, 5, 3, "a - b - c")
        self.assertEqual(result_int, 2)
        self.assertEqual(result_float, 2.0)
        
        # 乘法
        result_int, result_float = self.node.calculate_expression(2, 3, 4, "a * b * c")
        self.assertEqual(result_int, 24)
        self.assertEqual(result_float, 24.0)
        
        # 除法
        result_int, result_float = self.node.calculate_expression(20, 4, 2, "a / b / c")
        self.assertEqual(result_int, 2)
        self.assertEqual(result_float, 2.5)
    
    def test_math_functions(self):
        """测试数学函数"""
        # 平方根
        result_int, result_float = self.node.calculate_expression(16, 0, 0, "sqrt(a)")
        self.assertEqual(result_int, 4)
        self.assertEqual(result_float, 4.0)
        
        # 幂运算
        result_int, result_float = self.node.calculate_expression(2, 3, 0, "pow(a, b)")
        self.assertEqual(result_int, 8)
        self.assertEqual(result_float, 8.0)
        
        # 绝对值
        result_int, result_float = self.node.calculate_expression(-5, 0, 0, "abs(a)")
        self.assertEqual(result_int, 5)
        self.assertEqual(result_float, 5.0)
        
        # 最大最小值
        result_int, result_float = self.node.calculate_expression(10, 5, 15, "max(a, b, c)")
        self.assertEqual(result_int, 15)
        self.assertEqual(result_float, 15.0)
        
        result_int, result_float = self.node.calculate_expression(10, 5, 15, "min(a, b, c)")
        self.assertEqual(result_int, 5)
        self.assertEqual(result_float, 5.0)
    
    def test_rounding_functions(self):
        """测试取整函数"""
        # ceil函数
        result_int, result_float = self.node.calculate_expression(3.2, 0, 0, "ceil(a)")
        self.assertEqual(result_int, 4)
        self.assertEqual(result_float, 4.0)
        
        # floor函数
        result_int, result_float = self.node.calculate_expression(3.8, 0, 0, "floor(a)")
        self.assertEqual(result_int, 3)
        self.assertEqual(result_float, 3.0)
        
        # round函数
        result_int, result_float = self.node.calculate_expression(3.6, 0, 0, "round(a)")
        self.assertEqual(result_int, 4)
        self.assertEqual(result_float, 4.0)
        
        result_int, result_float = self.node.calculate_expression(3.4, 0, 0, "round(a)")
        self.assertEqual(result_int, 3)
        self.assertEqual(result_float, 3.0)
    
    def test_trigonometric_functions(self):
        """测试三角函数"""
        import math
        
        # sin函数
        result_int, result_float = self.node.calculate_expression(math.pi/2, 0, 0, "sin(a)")
        self.assertAlmostEqual(result_float, 1.0, places=5)
        
        # cos函数  
        result_int, result_float = self.node.calculate_expression(0, 0, 0, "cos(a)")
        self.assertAlmostEqual(result_float, 1.0, places=5)
        
        # 使用常数pi
        result_int, result_float = self.node.calculate_expression(0, 0, 0, "sin(pi/2)")
        self.assertAlmostEqual(result_float, 1.0, places=5)
    
    def test_complex_expressions(self):
        """测试复杂表达式"""
        # 复合运算
        result_int, result_float = self.node.calculate_expression(3, 4, 5, "sqrt(a*a + b*b)")
        self.assertEqual(result_int, 5)
        self.assertEqual(result_float, 5.0)
        
        # 多层嵌套 - sqrt(8) = 2.828..., pow(2.828, 2) = 8, 8 + 3 = 11
        result_int, result_float = self.node.calculate_expression(8, 2, 3, "pow(sqrt(a), b) + c")
        self.assertEqual(result_int, 11)
        self.assertAlmostEqual(result_float, 11.0, places=1)
        
        # 使用数学常数
        result_int, result_float = self.node.calculate_expression(1, 0, 0, "a * pi")
        self.assertAlmostEqual(result_float, math.pi, places=5)
    
    def test_error_handling(self):
        """测试错误处理"""
        # 除零错误
        result_int, result_float = self.node.calculate_expression(10, 0, 0, "a / b")
        self.assertEqual(result_int, 0)
        self.assertEqual(result_float, 0.0)
        
        # 无效表达式
        result_int, result_float = self.node.calculate_expression(1, 2, 3, "invalid_function(a)")
        self.assertEqual(result_int, 0)
        self.assertEqual(result_float, 0.0)
        
        # 非法导入
        result_int, result_float = self.node.calculate_expression(1, 2, 3, "import os")
        self.assertEqual(result_int, 0)
        self.assertEqual(result_float, 0.0)
    
    def test_input_types(self):
        """测试输入类型定义"""
        input_types = PopoMathExpressionNode.INPUT_TYPES()
        
        # 检查必需输入
        self.assertIn("required", input_types)
        required = input_types["required"]
        
        # 检查a, b, c参数
        for param in ["a", "b", "c"]:
            self.assertIn(param, required)
            self.assertEqual(required[param][0], "FLOAT")
        
        # 检查表达式参数
        self.assertIn("expression", required)
        self.assertEqual(required["expression"][0], "STRING")
    
    def test_node_attributes(self):
        """测试节点属性"""
        self.assertEqual(PopoMathExpressionNode.RETURN_TYPES, ("INT", "FLOAT"))
        self.assertEqual(PopoMathExpressionNode.RETURN_NAMES, ("result_int", "result_float"))
        self.assertEqual(PopoMathExpressionNode.FUNCTION, "calculate_expression")
        self.assertEqual(PopoMathExpressionNode.CATEGORY, "popo-utility")
    
    def test_security(self):
        """测试安全性"""
        node = PopoMathExpressionNode()
        
        # 测试危险操作被阻止
        dangerous_expressions = [
            "__import__('os')",
            "eval('1+1')",
            "exec('print(1)')",
            "open('file.txt')",
            "globals()",
            "locals()",
        ]
        
        for expr in dangerous_expressions:
            result_int, result_float = node.calculate_expression(1, 2, 3, expr)
            self.assertEqual(result_int, 0)
            self.assertEqual(result_float, 0.0)


if __name__ == "__main__":
    # 运行测试
    print("开始测试PopoMathExpressionNode...")
    unittest.main(verbosity=2)