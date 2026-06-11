# QUESTIONS

## windows 终端如何创建符号链接

在 Windows 终端（cmd）中，使用 `mklink` 命令创建符号链接：

```cmd
mklink [[/D] | [/H] | [/J]] <链接名> <目标路径>
```

- 不加参数：创建**文件符号链接**。
- `/D`：创建**目录符号链接**。
- `/H`：创建硬链接（非符号链接）。
- `/J`：创建目录联接（junction）。

示例：

```cmd
mklink link.txt C:\path\to\real.txt
mklink /D linkdir C:\path\to\realdir
```

在 PowerShell 中，可用 `New-Item`：

```powershell
New-Item -ItemType SymbolicLink -Path "link" -Target "C:\path\to\target"
```

注意：
- 默认需要**管理员权限**（除非启用开发人员模式：设置 → 隐私和安全性 → 开发者选项 → 开启“开发人员模式”）。
- 路径建议使用绝对路径或正确的相对路径。

