-- 定义一个函数来获取剪贴板中的文本内容
on getClipboardText()
	try
		set theText to the clipboard as text
	on error
		set theText to ""
	end try
	return theText
end getClipboardText

-- 定义一个函数来检查是否有朗读进程正在运行
on isSpeaking()
	try
		do shell script "pgrep -x say"
		return true
	on error
		return false
	end try
end isSpeaking

-- 初始化变量
set previousText to ""
set isReading to false

-- 创建一个循环来持续监控剪贴板内容
repeat
	-- 获取当前剪贴板的文本内容
	set currentText to getClipboardText()
	
	-- 检查剪贴板内容是否有变化
	if currentText is not equal to previousText then
		-- 如果正在朗读，则停止朗读
		if isReading and isSpeaking() then
			do shell script "killall say"
			-- 等待 say 进程完全退出
			repeat while isSpeaking()
				delay 0.1
			end repeat
			set isReading to false
		end if
		
		-- 朗读新的文本内容
		if currentText is not "" then
			-- 使用后台运行来朗读文本，语速调慢
			-- 为避免命令行长度或换行导致的截断，将文本通过 printf 管道传给 say，并使用 nohup 后台运行
			do shell script "printf %s " & quoted form of currentText & " | nohup say -r 120 >/dev/null 2>&1 &"
			set isReading to true
		end if
		
		-- 更新上一次的文本内容
		set previousText to currentText
	end if
	
	-- 等待一小段时间以降低系统资源使用
	delay 0.5
end repeat