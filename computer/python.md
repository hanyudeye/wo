--

# 3. 数据类型

## 字符串（str）

```python
name = "Alice"
```

## 整数（int）

```python
age = 25
```

## 浮点数（float）

```python
price = 9.99
```

## 布尔值（bool）

```python
is_student = True
is_admin = False
```

查看类型：

```python
print(type(age))
```

输出：

```text
<class 'int'>
```

---

# 4. 输入和输出

## 输出

```python
print("Hello")
```

## 输入

```python
name = input("请输入姓名：")
print(name)
```

输入内容默认是字符串。

例如：

```python
age = int(input("请输入年龄："))
```

转换为整数。

---

# 5. 运算符

## 算术运算

```python
a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
```

结果：

```text
13
7
30
3.333333
```

---

## 取余

```python
print(10 % 3)
```

结果：

```text
1
```

常用于判断奇偶数：

```python
if num % 2 == 0:
    print("偶数")
```

---

## 幂运算

```python
print(2 ** 3)
```

结果：

```text
8
```

---

# 6. 条件判断

## if

```python
age = 18

if age >= 18:
    print("成年人")
```

---

## if else

```python
age = 15

if age >= 18:
    print("成年人")
else:
    print("未成年人")
```

---

## if elif else

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 60:
    print("C")
else:
    print("D")
```

---

# 7. 循环

## while

```python
i = 1

while i <= 5:
    print(i)
    i += 1
```

输出：

```text
1
2
3
4
5
```

---

## for

```python
for i in range(5):
    print(i)
```

输出：

```text
0
1
2
3
4
```

---

常见写法：

```python
for i in range(1, 6):
    print(i)
```

输出：

```text
1
2
3
4
5
```

---

# 8. 列表（List）

列表相当于数组。

```python
fruits = ["apple", "banana", "orange"]
```

访问元素：

```python
print(fruits[0])
```

输出：

```text
apple
```

---

添加元素：

```python
fruits.append("grape")
```

删除元素：

```python
fruits.remove("banana")
```

长度：

```python
print(len(fruits))
```

---

遍历：

```python
for fruit in fruits:
    print(fruit)
```

---

# 9. 元组（Tuple）

元组创建后不能修改。

```python
point = (10, 20)
```

访问：

```python
print(point[0])
```

---

适合存放固定数据：

```python
rgb = (255, 255, 255)
```

---

# 10. 字典（Dictionary）

字典是键值对结构。

```python
user = {
    "name": "Tom",
    "age": 20
}
```

获取：

```python
print(user["name"])
```

输出：

```text
Tom
```

---

新增：

```python
user["city"] = "Shanghai"
```

修改：

```python
user["age"] = 21
```

---

遍历：

```python
for key, value in user.items():
    print(key, value)
```

---

# 11. 函数

函数用于封装代码。

```python
def hello():
    print("Hello")
```

调用：

```python
hello()
```

---

带参数：

```python
def greet(name):
    print("Hello", name)

greet("Tom")
```

---

返回值：

```python
def add(a, b):
    return a + b

result = add(3, 5)

print(result)
```

---

# 12. 字符串常用操作

长度：

```python
len("Python")
```

结果：

```text
6
```

---

转大写：

```python
name.upper()
```

转小写：

```python
name.lower()
```

---

替换：

```python
text.replace("hello", "hi")
```

---

切片：

```python
text = "Python"

print(text[0:3])
```

结果：

```text
Pyt
```

---

# 13. 文件读写

## 写文件

```python
with open("test.txt", "w") as f:
    f.write("Hello")
```

---

## 读文件

```python
with open("test.txt", "r") as f:
    content = f.read()

print(content)
```

---

# 14. 异常处理

避免程序崩溃。

```python
try:
    num = int(input("输入数字："))
    print(num)
except:
    print("输入错误")
```

更规范：

```python
try:
    num = int(input())
except ValueError:
    print("不是数字")
```

---

# 15. 模块

Python 的代码库称为模块。

导入：

```python
import math

print(math.sqrt(16))
```

结果：

```text
4.0
```

---

随机数：

```python
import random

print(random.randint(1, 100))
```

---

# 16. 面向对象（OOP）

定义类：

```python
class Dog:

    def __init__(self, name):
        self.name = name

    def bark(self):
        print(self.name + " 汪汪叫")
```

创建对象：

```python
dog = Dog("旺财")

dog.bark()
```

输出：

```text
旺财 汪汪叫
```

---

# 17. 实战：猜数字游戏

```python
import random

answer = random.randint(1, 100)

while True:

    guess = int(input("猜数字："))

    if guess > answer:
        print("大了")

    elif guess < answer:
        print("小了")

    else:
        print("猜对了")
        break
```

---

# 18. 实战：批量重命名文件

```python
import os

files = os.listdir("images")

count = 1

for file in files:

    old_name = f"images/{file}"
    new_name = f"images/img_{count}.jpg"

    os.rename(old_name, new_name)

    count += 1
```

---

# 19. 实战：网页抓取

安装：

```bash
pip install requests
```

代码：

```python
import requests

url = "https://example.com"

response = requests.get(url)

print(response.text)
```

---

# 20. 实战：自动化办公 Excel

安装：

```bash
pip install openpyxl
```

读取：

```python
from openpyxl import load_workbook

wb = load_workbook("data.xlsx")

sheet = wb.active

print(sheet["A1"].value)
```

---

# 下一步学习路线

如果你的目标是：

### 自动化办公

学习：

* Python基础
* 文件处理
* openpyxl
* pandas
* pyautogui

### AI开发

学习：

* Python基础
* NumPy
* Pandas
* PyTorch
* LLM API调用

### Web开发

学习：

* Python基础
* HTML
* CSS
* JavaScript
* Flask
* Django

### 运维自动化

学习：

* Linux
* Python
* Shell
* Ansible
* Docker

---

对于大多数初学者，建议按以下顺序：

```text
Python基础
↓
函数
↓
列表和字典
↓
文件处理
↓
异常处理
↓
模块
↓
面向对象
↓
自动化脚本
↓
Web爬虫
↓
数据库
↓
项目实战
```

学完这些内容后，已经具备编写实用工具、自动化脚本和入门 AI 项目的能力。
