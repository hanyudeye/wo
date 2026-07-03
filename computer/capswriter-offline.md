# 添加词汇

你现在看的这个 **CapsWriter-Offline** 项目已经在 README 里写得很清楚：它的“添加词汇”功能其实叫 **热词替换（Hot Words）**，通过两个文件来实现：

---

## 🔥 **一、热词替换（hot.txt）——添加你自己的词汇**
这是最常用的方式，用来解决“识别不到某些生僻词、专有名词”的问题。

### **文件位置**
在项目根目录里有一个文件：

```
hot.txt
```

### **怎么写？**
你只需要把想要强制替换的词写进去，每行一个，例如：

```
OpenAI
CapsWriter
无锡太湖学院
量子纠缠
```

### **工作原理（来自页面内容）**  
CapsWriter 会用 **音素模糊匹配**，当识别结果与某个热词的相似度超过阈值，就会自动替换成你写的词。  
  [github.com](https://github.com/HaujetZhao/CapsWriter-Offline)

---

## 🧩 **二、规则替换（hot-rule.txt）——更强的自定义**
如果你想做更复杂的替换，比如：

- 正则表达式替换  
- 简单的“等号规则”替换（A= B）

就写在：

```
hot-rule.txt
```

### 示例：

```
AI=人工智能
CapsWriter=语音输入神器
```

或使用正则：

```
(苹果|Apple)=Apple公司
```

规则替换比热词更强，适合你想精准控制输出的场景。  
  [github.com](https://github.com/HaujetZhao/CapsWriter-Offline)

---

## 🛠 **三、在哪里编辑？**
你可以直接：

- 在软件根目录找到 `hot.txt` 和 `hot-rule.txt`
- 用记事本、VSCode 等编辑器打开
- 保存后立即生效（无需重启）

---

## 🧪 **四、如何快速验证热词是否生效？**
CapsWriter 会把你的每次语音识别结果保存到：

```
年/月/assets/
```

你可以：

1. 录一句包含热词的语音  
2. 去 assets 文件夹看识别结果是否被替换  
  [github.com](https://github.com/HaujetZhao/CapsWriter-Offline)
