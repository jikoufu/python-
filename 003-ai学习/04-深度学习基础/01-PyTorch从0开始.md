# PyTorch 从 0 开始

> **一句话先说清楚**：PyTorch 干的事，就是帮你做两件人手做不动的事——**自动求导**和**用 GPU 算大矩阵**。学会它的本质，是学会"准备数据 → 搭网络 → 定义损失 → 反复让模型自己改错"这一套循环，而这套循环，所有深度学习项目都长一个样。

---

## 学习路线总览（总）

很多人学 PyTorch 失败，是因为一上来就抄一个图像分类的完整代码，看着能跑，但每一行为什么这么写完全不懂。

正确的顺序是**从底层往上搭**，每一层都知道它解决了什么问题：

```
第1站：Tensor（张量）        —— PyTorch 的"数据原子"，一切的基础
   ↓
第2站：Autograd（自动求导）   —— PyTorch 的"魔法核心"，凭什么模型能自己学
   ↓
第3站：手写一个线性回归       —— 用前两站的知识，不用任何高级API，吃透训练循环
   ↓
第4站：nn.Module（搭网络）    —— 用官方积木重写，理解封装解决了什么
   ↓
第5站：完整训练流程          —— Dataset/DataLoader/优化器/损失函数 五件套
   ↓
第6站：实战 —— 手写数字识别   —— 第一个真正"有用"的神经网络
   ↓
第7站：GPU / 保存模型 / 调试   —— 工程化，让它能用起来
```

**核心心法**：第3站（手写线性回归）是整条路线的命脉。只要你能不靠任何高级 API 写出一个会自己学习的模型，后面全是"换更方便的工具"而已。

---

## 准备工作：安装

```bash
# CPU 版本（学习够用）
pip install torch torchvision

# 如果你有 NVIDIA 显卡，去官网选 CUDA 版本：
# https://pytorch.org/get-started/locally/
```

验证安装：

```python
import torch
print(torch.__version__)              # 看版本
print(torch.cuda.is_available())      # True = 能用 GPU，False = 只能用 CPU（学习无所谓）
```

---

## 第1站：Tensor（张量）—— 数据原子（分）

### 它是什么

**Tensor（张量）就是多维数组**，和 NumPy 的 `ndarray` 几乎一样。你完全可以把它理解为"会用 GPU、会自动求导的 NumPy 数组"。

```
标量（0维）：  5
向量（1维）：  [1, 2, 3]
矩阵（2维）：  [[1, 2], [3, 4]]
3维及以上：   一摞矩阵（比如一批图片）
```

### 创建 Tensor

```python
import torch

# 直接从数据创建
a = torch.tensor([1, 2, 3])
b = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

# 常用快捷方式
zeros = torch.zeros(2, 3)        # 2行3列的全0
ones = torch.ones(2, 3)          # 全1
rand = torch.randn(2, 3)         # 标准正态分布的随机数（搭网络初始化常用）
arange = torch.arange(0, 10)     # 0~9

print(b.shape)      # torch.Size([2, 2])  —— 形状，最常看的属性
print(b.dtype)      # torch.float32       —— 数据类型
```

### 基本运算

```python
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])

print(x + y)            # 逐元素加 [5, 7, 9]
print(x * y)            # 逐元素乘 [4, 10, 18]
print(x.sum())          # 求和 6.0
print(x.mean())         # 均值 2.0

# 矩阵乘法（深度学习的核心运算）
m1 = torch.randn(2, 3)
m2 = torch.randn(3, 4)
print((m1 @ m2).shape)  # torch.Size([2, 4])  —— @ 是矩阵乘
```

### 形状变换（极其常用）

神经网络里 90% 的报错都是形状对不上，所以一定要熟：

```python
x = torch.arange(12)            # [0,1,2,...,11]  形状(12,)
print(x.reshape(3, 4))          # 变成 3行4列
print(x.reshape(3, 4).T)        # 转置
print(x.reshape(2, 2, 3).shape) # 变3维 torch.Size([2, 2, 3])

# -1 表示"这一维你帮我算"
print(x.reshape(2, -1).shape)   # torch.Size([2, 6])
```

### 和 NumPy 互转

```python
import numpy as np

np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)   # numpy → tensor
back = tensor.numpy()                  # tensor → numpy
```

> **本站小结**：Tensor 就是 NumPy 数组的升级版。先把"创建、运算、变形状"练熟，因为后面所有数据都是 Tensor。

---

## 第2站：Autograd（自动求导）—— 魔法核心（分）

### 为什么这是 PyTorch 的灵魂

神经网络"学习"的本质，是**不断微调参数，让预测误差变小**。要知道"往哪个方向调"，就得算误差对每个参数的**导数（梯度）**。

一个真实网络有几百万个参数，手算导数是不可能的。**PyTorch 的 autograd 能自动帮你算出所有梯度**——这就是它最值钱的功能。

### 怎么用：requires_grad

```python
# 告诉 PyTorch：这个变量我要对它求导，请帮我记录
x = torch.tensor(2.0, requires_grad=True)

# 定义一个函数 y = x²
y = x ** 2

# 自动求导：算 dy/dx
y.backward()

# 查看梯度
print(x.grad)    # 4.0   （因为 dy/dx = 2x = 2*2 = 4）
```

**发生了什么？**
1. 你设 `requires_grad=True`，PyTorch 开始悄悄记录所有对 x 的运算（构建"计算图"）
2. 调 `y.backward()`，PyTorch 沿着记录反向走一遍，自动算出导数
3. 结果存在 `x.grad` 里

### 多变量的例子

```python
x = torch.tensor(3.0, requires_grad=True)
w = torch.tensor(4.0, requires_grad=True)

# z = w * x + 2
z = w * x + 2
z.backward()

print(x.grad)    # 4.0   (dz/dx = w = 4)
print(w.grad)    # 3.0   (dz/dw = x = 3)
```

**关键理解**：你只管正向写公式，反向的导数 PyTorch 全包了。这就是为什么你能搭任意复杂的网络而不用手算一个导数。

> **本站小结**：`requires_grad=True` 让 PyTorch 盯着一个变量，`backward()` 自动算梯度，结果存在 `.grad`。整个深度学习就建立在这一个机制上。

---

## 第3站：手写线性回归 —— 吃透训练循环（分）⭐

**这一站是整条路线最重要的部分。** 我们不用任何高级 API，纯手工训练一个模型，把"模型如何自己学习"彻底搞懂。

### 任务

我们造一批假数据，真实规律是 `y = 2x + 1`。然后让模型在**不知道这个规律**的情况下，自己从数据里学出 `w≈2`、`b≈1`。

```python
import torch

# ===== 1. 准备数据：真实规律 y = 2x + 1 =====
X = torch.randn(100, 1)              # 100个样本
y_true = 2 * X + 1 + 0.1 * torch.randn(100, 1)   # 加一点噪声，更真实

# ===== 2. 初始化参数（随机猜一个起点）=====
w = torch.randn(1, requires_grad=True)   # 要学的权重
b = torch.randn(1, requires_grad=True)   # 要学的偏置

learning_rate = 0.1     # 学习率：每次调多大步

# ===== 3. 训练循环（核心中的核心）=====
for epoch in range(100):
    # (a) 前向传播：用当前参数做预测
    y_pred = w * X + b

    # (b) 计算损失：预测和真实差多少（均方误差）
    loss = ((y_pred - y_true) ** 2).mean()

    # (c) 反向传播：自动算出 loss 对 w 和 b 的梯度
    loss.backward()

    # (d) 更新参数：朝着让损失变小的方向调
    with torch.no_grad():           # 这步不需要被求导记录
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad

    # (e) 清空梯度（重要！否则梯度会累加）
    w.grad.zero_()
    b.grad.zero_()

    if epoch % 10 == 0:
        print(f"第{epoch}轮  损失={loss.item():.4f}  w={w.item():.3f}  b={b.item():.3f}")

print(f"\n学到的规律：y = {w.item():.2f}x + {b.item():.2f}")
print("真实的规律：y = 2.00x + 1.00")
```

运行后你会看到 `w` 慢慢逼近 2，`b` 慢慢逼近 1。**模型真的自己学会了！**

### 把训练循环刻进脑子里

这五步，是**所有**深度学习训练的固定套路，一辈子都不会变：

```
for 每一轮:
    1. 前向传播：y_pred = 模型(输入)        # 做预测
    2. 算损失：  loss = 损失函数(预测, 真实)  # 评估错得多离谱
    3. loss.backward()                     # 反向求梯度
    4. 更新参数：参数 -= 学习率 * 梯度        # 朝正确方向挪一小步
    5. 梯度清零：optimizer.zero_grad()      # 为下一轮做准备
```

后面无论网络多复杂，循环结构永远是这五步。**只要这一站懂了，深度学习你就入门了。**

### 三个新手必踩的坑

| 坑 | 后果 | 原因 |
|----|------|------|
| 忘了 `grad.zero_()` | 损失乱跳、不收敛 | PyTorch 默认累加梯度，不清零会越加越大 |
| 更新参数没包 `torch.no_grad()` | 报错或行为异常 | 更新参数这步不该被记录进计算图 |
| 学习率设太大（如 10） | 损失变成 nan/爆炸 | 步子迈太大，直接跳过最低点飞出去 |

---

## 第4站：nn.Module —— 用官方积木搭网络（分）

第3站我们手动管理 `w` 和 `b`。但真实网络有几百万参数，手动管理是噩梦。PyTorch 提供 `nn.Module` 帮你封装。

### 同样的线性回归，用 nn 重写

```python
import torch
import torch.nn as nn

# ===== 用官方的"线性层"代替手写的 w*x+b =====
model = nn.Linear(in_features=1, out_features=1)   # 输入1维，输出1维，w和b它自动管

# ===== 用官方的损失函数和优化器 =====
loss_fn = nn.MSELoss()                                    # 均方误差，代替手写
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)  # 优化器，代替手动更新

# ===== 训练循环：还是那五步！=====
for epoch in range(100):
    y_pred = model(X)               # 1. 前向（直接调 model）
    loss = loss_fn(y_pred, y_true)  # 2. 算损失

    optimizer.zero_grad()           # 5. 清零（习惯放最前）
    loss.backward()                 # 3. 反向
    optimizer.step()                # 4. 更新（一行搞定所有参数！）

    if epoch % 10 == 0:
        print(f"第{epoch}轮  损失={loss.item():.4f}")
```

对比第3站，你会发现：**五步循环一模一样**，只是：
- `w*X+b` → `model(X)`
- 手写损失 → `loss_fn`
- 手动更新+清零 → `optimizer.step()` + `optimizer.zero_grad()`

这就是 nn.Module 的价值：**把繁琐的参数管理自动化，但训练逻辑不变。**

### 搭一个多层网络

真正的"深度"学习，是堆叠多层 + 非线性激活：

```python
class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 128),    # 第1层：784维输入 → 128维
            nn.ReLU(),              # 激活函数：引入非线性（关键！）
            nn.Linear(128, 64),     # 第2层
            nn.ReLU(),
            nn.Linear(64, 10),      # 输出层：10个类别
        )

    def forward(self, x):
        return self.net(x)          # 数据怎么流过网络

model = MyNet()
print(model)
```

> **为什么要 ReLU？** 如果只堆线性层，再多层叠起来数学上还是一条直线，学不会复杂规律。ReLU 这种激活函数引入"弯曲"，网络才能拟合复杂模式。

---

## 第5站：完整训练流程五件套（分）

一个工程化的训练，标配这五样东西：

```
1. Dataset      —— 定义"一条数据长什么样"
2. DataLoader   —— 自动分批、打乱、并行加载
3. Model        —— 网络结构（第4站）
4. Loss         —— 损失函数
5. Optimizer    —— 优化器
```

### Dataset 和 DataLoader

数据通常很大，不能一次全塞进模型，要**分批（batch）**喂：

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)            # 一共多少条

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]   # 取第 idx 条

dataset = MyDataset(X, y_true)
loader = DataLoader(dataset, batch_size=16, shuffle=True)
#                              每批16条      每轮打乱顺序

# 用法：
for batch_X, batch_y in loader:
    # 每次拿到16条数据
    ...
```

为什么要分批？
- **内存装得下**：百万张图片不可能一次性加载
- **训练更稳**：每批算一次梯度，更新更频繁，收敛更快

---

## 第6站：实战 —— 手写数字识别（分）⭐

把前面所有知识合起来，做第一个真正有用的网络：识别 0~9 的手写数字（MNIST 数据集）。

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# ===== 1. 准备数据（torchvision 自带 MNIST）=====
transform = transforms.ToTensor()    # 把图片转成 Tensor
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data  = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader  = DataLoader(test_data, batch_size=64)

# ===== 2. 搭网络（28x28=784 像素输入 → 10 个数字输出）=====
class DigitNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()           # 把 28x28 图片拍平成 784
        self.net = nn.Sequential(
            nn.Linear(784, 128), nn.ReLU(),
            nn.Linear(128, 64),  nn.ReLU(),
            nn.Linear(64, 10),
        )

    def forward(self, x):
        return self.net(self.flatten(x))

model = DigitNet()

# ===== 3. 损失 + 优化器 =====
loss_fn = nn.CrossEntropyLoss()                          # 分类任务专用损失
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Adam：比 SGD 更好用的优化器

# ===== 4. 训练（还是那五步！）=====
for epoch in range(3):
    for images, labels in train_loader:
        preds = model(images)              # 1. 前向
        loss = loss_fn(preds, labels)      # 2. 算损失
        optimizer.zero_grad()              # 5. 清零
        loss.backward()                    # 3. 反向
        optimizer.step()                   # 4. 更新
    print(f"第{epoch+1}轮完成  损失={loss.item():.4f}")

# ===== 5. 测试准确率 =====
correct = 0
total = 0
with torch.no_grad():                      # 测试不需要梯度
    for images, labels in test_loader:
        preds = model(images)
        predicted = preds.argmax(dim=1)    # 取概率最大的那个数字
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

print(f"测试准确率：{100 * correct / total:.2f}%")   # 通常能到 97% 左右
```

跑完你会得到一个准确率 97%+ 的手写数字识别器。**恭喜，你已经训练出第一个真正能用的神经网络了。**

---

## 第7站：工程化 —— GPU / 保存 / 调试（分）

### 用 GPU 加速

```python
# 自动选择设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = model.to(device)               # 模型搬到 GPU
# 训练时，数据也要搬过去：
for images, labels in train_loader:
    images, labels = images.to(device), labels.to(device)
    ...
```

记住规则：**模型和数据必须在同一个设备上**，否则报错。

### 保存和加载模型

```python
# 保存（只存参数，推荐）
torch.save(model.state_dict(), "model.pth")

# 加载
model = DigitNet()                          # 先建一个同样结构的空模型
model.load_state_dict(torch.load("model.pth"))
model.eval()                                # 切换到推理模式（重要）
```

> `model.eval()` vs `model.train()`：有些层（如 Dropout、BatchNorm）训练和推理时行为不同，切换模式很关键。

### 调试三板斧

```python
# 1. 形状对不上？打印 shape，这能解决一大半 bug
print(x.shape)

# 2. 损失变 nan？大概率学习率太大，调小试试
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

# 3. 损失不下降？检查：梯度清零了吗？学习率太小？数据/标签对齐了吗？
```

---

## 学习节奏建议（总）

| 阶段 | 内容 | 建议时间 | 完成标志 |
|------|------|---------|---------|
| 第1周 | 第1~2站：Tensor + Autograd | 3~4天 | 能解释 `backward()` 干了什么 |
| 第1周 | 第3站：手写线性回归 ⭐ | 2~3天 | **不看代码默写出训练五步** |
| 第2周 | 第4~5站：nn.Module + 数据加载 | 3~4天 | 能搭一个多层网络 |
| 第2周 | 第6站：手写数字识别 ⭐ | 2~3天 | 独立跑通，准确率 95%+ |
| 第3周 | 第7站 + 自己找数据集练手 | 持续 | 能改网络结构、调参 |

**最重要的一句话**：
> 不要急着堆复杂模型。把"第3站手写线性回归"和"第6站手写数字识别"这两个反复敲到能默写，PyTorch 你就真正入门了。剩下的（CNN、RNN、Transformer）都只是换网络结构，**训练那五步永远不变**。

---

## 本节重点

- PyTorch 帮你做两件事：**自动求导**（autograd）和 **GPU 加速大矩阵运算**
- **Tensor** 是数据原子，本质是"会求导的 NumPy 数组"，形状（shape）要烂熟
- **Autograd**：`requires_grad=True` 盯住变量，`backward()` 自动算梯度
- **训练五步**是整个深度学习的命脉，永远不变：
  前向 → 算损失 → 反向 → 更新 → 清零
- **nn.Module / 优化器 / DataLoader** 都只是把这五步自动化、工程化的工具
- 手写线性回归（第3站）和手写数字识别（第6站）是必须吃透的两个里程碑

---

## 自测问题

1. PyTorch 相比 NumPy，最核心的两个增强是什么？
2. `requires_grad=True` 和 `.backward()` 分别做了什么？
3. 不看代码，默写出训练循环的五个步骤。
4. 为什么每轮训练都要 `optimizer.zero_grad()`？不清零会怎样？
5. 网络里如果不加 ReLU 这种激活函数，会有什么问题？
6. 模型在 GPU、数据在 CPU，会发生什么？怎么解决？
7. `model.eval()` 和 `model.train()` 有什么区别，什么时候用哪个？
