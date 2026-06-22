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


## 强制删除文件夹

> 应对挖矿程序，有保护权限的 很难删除的文件

```
$dir = 'C:\ProgramData\egJ1vm0Y'

# 结束从该目录启动的进程
Get-CimInstance Win32_Process | Where-Object {
    $_.ExecutablePath -like "$dir\*"
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

# 清除属性、夺权、重置权限
attrib -r -s -h "$dir\*" /s /d
takeown /f "$dir" /r /d y
icacls "$dir" /reset /t /c
icacls "$dir" /grant "Administrators:(OI)(CI)F" /t /c

# 删除目录和其中所有文件
Remove-Item -LiteralPath $dir -Recurse -Force

```


## 强制删除文件


```
$file = 'C:\ProgramData\5lFVtpUB.exe'

# 若该 exe 正在运行，先按完整路径结束进程
Get-CimInstance Win32_Process | Where-Object {
    $_.ExecutablePath -eq $file
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

# 去除属性、取得所有权、授予当前管理员组完全控制
attrib -r -s -h $file
takeown /f $file
icacls $file /grant 'Administrators:F'

# 仅删除这个文件
Remove-Item -LiteralPath $file -Force

```

