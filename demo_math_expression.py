#!/usr/bin/env python3
"""
Popo Math Expression Node 使用示例
展示数学表达式节点的各种用法
"""

import sys
import os
from unittest.mock import MagicMock

# 模拟ComfyUI环境
sys.modules['torch'] = MagicMock()
sys.modules['numpy'] = MagicMock()

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nodes_direct import PopoMathExpressionNode


def demo_math_expressions():
    """演示数学表达式节点的使用"""
    
    print("🧮 Popo Math Expression Node 使用示例")
    print("=" * 50)
    
    node = PopoMathExpressionNode()
    
    # 示例1: 基础算术运算
    print("\n📊 基础算术运算示例:")
    examples_basic = [
        (10, 5, 3, "a + b + c", "三数相加"),
        (10, 5, 3, "a - b - c", "连续减法"), 
        (10, 5, 3, "a * b / c", "乘除混合"),
        (2, 3, 4, "a ** b + c", "幂运算加法"),
        (100, 3, 0, "a % b", "取模运算"),
    ]
    
    for a, b, c, expr, desc in examples_basic:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float}")
        print()
    
    # 示例2: 数学函数
    print("\n📐 数学函数示例:")
    examples_math = [
        (16, 0, 0, "sqrt(a)", "平方根"),
        (3.7, 0, 0, "ceil(a)", "向上取整"),
        (3.7, 0, 0, "floor(a)", "向下取整"),
        (3.14159, 2, 0, "round(a, b)", "四舍五入到指定位数"),
        (-5.5, 0, 0, "abs(a)", "绝对值"),
        (2, 8, 0, "pow(a, b)", "幂运算"),
    ]
    
    for a, b, c, expr, desc in examples_math:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float}")
        print()
    
    # 示例3: 三角函数
    print("\n📏 三角函数示例:")
    examples_trig = [
        (0, 0, 0, "sin(pi/2)", "sin(π/2) = 1"),
        (0, 0, 0, "cos(0)", "cos(0) = 1"),
        (0, 0, 0, "tan(pi/4)", "tan(π/4) ≈ 1"),
        (30, 0, 0, "sin(radians(a))", "30度角的正弦值"),
        (1, 0, 0, "degrees(asin(a))", "反正弦函数转角度"),
    ]
    
    for a, b, c, expr, desc in examples_trig:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float:.4f}")
        print()
    
    # 示例4: 复杂表达式
    print("\n🔬 复杂表达式示例:")
    examples_complex = [
        (3, 4, 0, "sqrt(a*a + b*b)", "计算斜边长度"),
        (10, 20, 5, "min(a, b) + max(b, c)", "最小值加最大值"),
        (100, 3, 0, "a // b + a % b", "整除和取模的和"),
        (2, 3, 1, "pow(a, b) * c + sqrt(a+b)", "复合运算"),
        (1, 0, 0, "factorial(5) / pow(2, a)", "阶乘除以幂"),
        (45, 0, 0, "sin(radians(a)) + cos(radians(a))", "三角函数组合"),
    ]
    
    for a, b, c, expr, desc in examples_complex:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float:.4f}")
        print()
    
    # 示例5: 使用数学常数
    print("\n🔢 数学常数示例:")
    examples_constants = [
        (1, 0, 0, "a * pi", "π的倍数"),
        (1, 0, 0, "a * e", "自然常数e"),
        (2, 0, 0, "a * tau", "τ = 2π"),
        (0, 0, 0, "pi / 4", "π/4的值"),
        (1, 0, 0, "log(e)", "ln(e) = 1"),
        (10, 0, 0, "log10(a)", "以10为底的对数"),
    ]
    
    for a, b, c, expr, desc in examples_constants:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float:.4f}")
        print()
    
    # 示例6: 条件表达式（使用三元运算符）
    print("\n🔀 条件表达式示例:")
    examples_conditional = [
        (10, 5, 0, "a if a > b else b", "取较大值"),
        (3, 5, 0, "a if a > b else b", "取较大值"),
        (0, -5, 10, "abs(a) if a != 0 else c", "非零取绝对值，否则用c"),
        (16, 0, 0, "sqrt(a) if a >= 0 else 0", "安全平方根"),
    ]
    
    for a, b, c, expr, desc in examples_conditional:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    a={a}, b={b}, c={c}")
        print(f"    结果: int={result_int}, float={result_float}")
        print()
    
    print("\n💡 提示:")
    print("  • 支持所有Python基础运算符: +, -, *, /, //, %, **")
    print("  • 支持所有math模块函数: sin, cos, tan, sqrt, log, exp等")
    print("  • 支持数学常数: pi, e, tau, inf, nan")
    print("  • 支持条件表达式和嵌套运算")
    print("  • 具有安全性检查，防止恶意代码执行")
    print("  • 结果同时输出整数和浮点数格式")


def demo_error_cases():
    """演示错误处理"""
    
    print("\n⚠️  错误处理示例:")
    print("=" * 30)
    
    node = PopoMathExpressionNode()
    
    error_cases = [
        (10, 0, 0, "a / b", "除零错误"),
        (1, 2, 3, "undefined_function(a)", "未定义函数"),
        (-1, 0, 0, "sqrt(a)", "负数开方"),
        (1, 2, 3, "import os", "危险导入"),
        (1, 2, 3, "eval('1+1')", "嵌套eval"),
    ]
    
    for a, b, c, expr, desc in error_cases:
        result_int, result_float = node.calculate_expression(a, b, c, expr)
        print(f"  {desc}: {expr}")
        print(f"    结果: int={result_int}, float={result_float}")
        print()


if __name__ == "__main__":
    demo_math_expressions()
    demo_error_cases()
    
    print("\n🎉 示例演示完成!")
    print("\n📖 在ComfyUI中使用:")
    print("  1. 右键 → Add Node → popo-utility → Popo Math Expression")
    print("  2. 设置a, b, c的数值")
    print("  3. 在expression输入框中输入数学表达式")
    print("  4. 连接输出到其他节点使用result_int或result_float")