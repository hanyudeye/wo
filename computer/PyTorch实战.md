## 我在学习 PyTorch ,告诉我 张量（Tensor）的概念，并能进行基本的创建、操作（维度变换、数学运算）



PyTorch中的**张量（Tensor）**是其最核心的数据结构，您可以将其理解为对 NumPy 数组的升级和扩展。简单来说，它是一种通用的、可多维度的容器，用于存储数据并在GPU上进行高效计算。

---

### 💡 一、 张量（Tensor）概念详解

#### 1. 什么是张量？
一个张量本质上就是一个**N阶数组**（N-dimensional array）。

*   **0 阶张量 (Scalar):** 单个数值（如 `5`）。
*   **1 阶张量 (Vector):** 一维列表（如 `[1, 2, 3]`）。
*   **2 阶张量 (Matrix):** 二维网格，通常我们说的“矩阵”就是二维张量。
*   **3 阶及以上张量:** 用于存储批处理数据或图像数据立方体（例如：`[Batch Size, Channels, Height, Width]`）。

#### 2. 为什么使用 PyTorch Tensor？
1.  **自动微分 (Autograd):** 这是最关键的能力。PyTorch可以追踪张量上的所有运算，并自动计算这些运算的梯度（导数），这使得模型训练成为可能。
2.  **GPU加速:** 张量天然支持将数据和计算转移到GPU上，极大地提升了深度学习的速度。

---

### 🧑‍💻 二、 基本操作与创建

```python
import torch
import numpy as np

# ====================
# 1. 创建张量 (Creation)
# ====================

# 从 Python 列表创建（最基础的方式）
tensor_from_list = torch.tensor([[[1, 2], [3, 4]]]) # 3D张量示例
print("--- 列表创建 ---")
print(tensor_from_list)


# 创建随机数张量 (常用的初始化方式)
# 使用torch.rand() 生成 [行数, 列数] 的均匀分布随机数
random_tensor = torch.rand(2, 3) # 2x3的矩阵
print("\n--- 随机创建 ---")
print(random_tensor)


# 创建全零或全一张量（常用于初始化权重）
zeros_tensor = torch.zeros(1, 4)
ones_tensor = torch.ones(2, 2)
print("\n--- 全零/全一 ---")
print("Zeros:", zeros_tensor)
```

#### ✨ 关键属性 (Attributes)：

创建张量后，您可以通过以下方式查看其核心信息：

*   `.shape` 或 `torch.size()`: 查看维度大小（例如：`torch.Size([2, 3])`）。
*   `.dtype`: 查看数据类型（如 `torch.float32`, `torch.long`）。
*   `.device`: 查看张量当前位于哪个设备上（`cpu` 或 `cuda`）。

---

### 🚀 三、 核心操作指南

#### 1. 数学运算 (Mathematical Operations)

##### A. **逐元素操作 (Element-wise Operations):**
如果两个张量的形状匹配，它们对应的每个元素会进行相同的运算。

```python
A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
B = torch.tensor([[5.0, 10.0], [1.0, 1.0]])

# 加法：对应元素相加
C_add = A + B
print("\n--- 逐元素相加 (A + B) ---")
print(C_add)

# 乘法：对应元素相乘
C_mul = A * torch.tensor([[2.0, 2.0], [2.0, 2.0]]) # 可以用广播机制
print("\n--- 逐元素相乘 (A * Scalar/Broadcast) ---")
print(C_mul)
```

##### B. **矩阵乘法 (Matrix Multiplication):**
在深度学习中，权重（Weight）和输入数据（Input）的计算通常是矩阵乘法。必须使用专门的函数或运算符 `@`。

*   **方法一：使用 `torch.matmul()` (推荐)**
*   **方法二：使用 `@` 符号 (Python 3.5+ 语法糖，推荐)**

```python
W = torch.rand(2, 3) # Weight: 2x3
X = torch.rand(1, 2) # Input: 1x2 -> 需要匹配维度进行乘法（实际操作通常需要展平或调整形状）

# 更标准的例子：假设我们要计算一个 (N x M) 的输出
A_matrix = torch.ones(5, 3)  # 5个样本，3个特征 (Batch Size=5, Features=3)
B_weight = torch.ones(3, 2) # 权重矩阵: 3个输入维度到2个输出维度

# 计算结果形状：(5 x 3) @ (3 x 2) -> (5 x 2)
Result = A_matrix @ B_weight 
print("\n--- 矩阵乘法 (A @ B) ---")
print(Result.shape) # 输出 (5, 2)
```

#### 2. 维度变换操作 (Dimension Transformations)

这些操作用于改变张量的“形状”（Shape），但不改变它包含的数据本身。

##### A. `torch.view()` 或 `tensor.reshape()` (重塑/调整形状)
用于将高维张量转换为指定形状的低维或高维张量。它们要求新形状的元素总数必须和原张量相等。`reshape`通常更灵活，因为它会自动处理连续性问题。

```python
# 创建一个 12 个元素的张量 (1, 1, ..., 1)
original = torch.arange(1, 13).float() # Shape: [12]

# 转换为 3行 x 4列 的矩阵
reshaped_tensor = original.view(3, 4)
print("\n--- 重塑 (View/Reshape): 1D -> 2D ---")
print(reshaped_tensor)
```

##### B. `torch.transpose()` 或 `.T` (转置 Transpose)
将矩阵的行和列互换。如果原始张量是 $M \times N$，转置后就是 $N \times M$。

```python
M = torch.arange(1, 7).float().view(2, 3) # 2x3矩阵
print("\n--- 原矩阵 M (2x3):\n", M)

# 方法一：使用 .T
M_transposed = M.T 

# 方法二：使用 torch.transpose(dim0, dim1)
# M_transposed = torch.transpose(M, 0, 1)

print("\n--- 转置后的矩阵 M.T (3x2):\n", M_transposed)
```

##### C. `torch.unsqueeze()` / `tensor[None,...]` (增加维度/Batch Dimension)
当一个形状为 `(N)` 的向量，需要作为批处理数据（即在模型输入中，它应该有 `(1, N)` 或 `(B, N)`）时，我们需要手动增加一个缺失的维度。

```python
# 原始张量: (4,) 的一维数据
vec = torch.rand(4)
print("\n--- 原始向量形状:", vec.shape) # torch.Size([4])

# 增加 Batch Dimension：使其形状变为 (1, 4)
batch_tensor = vec.unsqueeze(0) 
# 或者使用切片语法: batch_tensor = vec[None]
print("增加维度后形状:", batch_tensor.shape) # torch.Size([1, 4])
```
