# ERROR 1698 (28000): Access denied for user 'root'@'localhost'

**MySQL 8.0+ 后默认不让 root 用户用密码登录**，必须用**系统 root 权限**才能进。

## 一步进入 MySQL（必成功）
```bash
sudo mysql -u root
```
**不用输密码！** 直接就能进 MySQL 控制台。

---

## 二、修改 root 账号，允许密码登录
进入 MySQL 后，**依次执行下面 3 条命令**（复制粘贴）：

```sql
-- 1. 修改 root 密码认证方式
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的新密码';

-- 2. 刷新权限
FLUSH PRIVILEGES;

-- 3. 退出
exit;
```

示例（密码设为 123456）：
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
exit;
```

---

## 三、现在正常登录就可以了
```bash
mysql -u root -p
```
输入你刚才设置的密码，**就能成功登录**。

---

### 为什么会报这个错？
MySQL 8.0 默认使用 **auth_socket 认证**：
- 只有 **系统 root 用户（sudo）** 才能登录 MySQL root
- 普通用户即使输对密码也会报：**Access denied**

我们刚才的操作就是把它改成 **密码登录模式**。

# 给我  创建一个普通用户

## 1. 先进入 MySQL
```bash
sudo mysql -u root
```

## 2. 执行下面 SQL（复制整段即可）
把 `你的密码` 换成你想要的密码，比如 `123456`
```sql
CREATE USER 'testuser'@'localhost' IDENTIFIED BY '你的密码';

GRANT ALL PRIVILEGES ON *.* TO 'testuser'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;

exit;
```

## 3. 现在用普通用户登录
```bash
mysql -u testuser -p
```
输入你设置的密码就能进了。

---

### 如果你想更安全一点（只给某个库权限）
```sql
GRANT ALL PRIVILEGES ON 你的数据库名.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
```

# 数据库操作

创建数据库
CREATE DATABASE test;

GRANT ALL ON test.* to user(s);

第一行创建了一个名为“test”的数据库，假设你是数据库的管理员，第二行语句可以为
指定用户（或所有用户）提升权限，以便他们可以执行下述数据库操作。
使用数据库

USE test;
如果你已经登录一个数据库系统，但还没有选择你希望使用的数据库，这条简单的语句
可以让你指定一个数据库，用来执行数据库操作。

删除数据库
DROP DATABASE test;

## leftjoin

SELECT
    a.id,
    a.name,
    -- 拼接右表字段，逗号分隔
    GROUP_CONCAT(b.title SEPARATOR ',') AS title_list
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id
<!-- GROUP BY a.id,a.name; -->


# 软件 sqlite browse

---  美团拼接表格，业务员 ，t1 为业务表
SELECT a.商品ID ,a.服务门店名称,b.业务员 from t1 a left join 业务员 b on a.服务门店ID=b.服务门店ID;


