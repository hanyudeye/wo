## 每次登录都要开 GitHub app 验证？换默认方式

如果不想每次登录都打开 GitHub Mobile app 验证，可以在同一个 2FA 页面：

- **添加 Passkey（WebAuthn）**：Windows Hello / 手机 / 硬件钥匙，一键通过，比开 app 快
- **改用 TOTP app**（Authy、1Password、Google Authenticator）：扫码输 6 位码即可
- 取消 GitHub Mobile 2FA，或把上述某一种设为默认验证方式
- 登录时勾选「**Trust this device**」可让常用设备一段时间内免验证

只要保留至少一种可用方法，换掉 app 验证没影响。

**建议**：开启 2FA 后立刻把恢复码存到密码管理器，并同时配置 TOTP + Passkey 两种方式，避免单向依赖。

## 修下macbook屏幕
