
-- hammerspoon 脚本，用于在 macOS 上实现快捷键功能

-- 监听 Cmd+F，执行 killall say
hs.hotkey.bind({"cmd"}, "F", function()
    hs.execute("killall say")
end)

-- 激活名为“备忘录”的窗口
hs.hotkey.bind({"cmd"}, ".", function()
-- ，部分匹配窗口标题
    local win = hs.window.find("备忘录")
    if win then
        win:focus()
        win:raise()
    else
        hs.alert.show("未找到窗口：备忘录")
    end
end)

hs.hotkey.bind({"cmd"}, ",", function()
--  按应用名查找第一个窗口
    local app = hs.application.find("Emacs")
    if app then
        local win = app:mainWindow()
        if win then
            win:focus()
            win:raise()
        else
             hs.alert.show("未找到窗口：Emacs")
       end
    end
end)


