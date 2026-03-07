# GitHub 部署 - 快速指南

## 由于终端限制，请按以下步骤操作：

### 步骤 1: 创建 GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写信息:
   - Note: `Antonelli Deploy`
   - Expiration: `No expiration` (或选择 90 天)
   - 勾选以下权限:
     - ✅ `repo` (Full control of private repositories)
4. 点击 **"Generate token"**
5. **复制生成的 Token** (只显示一次！)

### 步骤 2: 在终端执行推送

打开终端，复制粘贴以下命令：

```bash
cd ~/.openclaw/workspace/projects/antonelli

# 配置 Git
git config user.name "Mason"
git config user.email "mason@example.com"

# 设置远程仓库
git remote remove origin 2>/dev/null
git remote add origin https://github.com/streitenjavis/antonelli.git

# 推送代码
git push -u origin main
```

当提示输入密码时，**粘贴你的 Personal Access Token** (不是 GitHub 密码)

### 步骤 3: 验证推送

推送成功后，访问：
https://github.com/streitenjavis/antonelli

应该能看到所有代码文件。

### 步骤 4: 部署到 Vercel

1. 访问 https://vercel.com/new
2. 导入 `antonelli` 仓库
3. 自动部署
4. 配置域名: `rss.shaojiujidi.com`

---

## 备选方案: 直接浏览器上传

如果不想使用 Token，可以直接在浏览器上传：

1. 访问 https://github.com/new
2. 创建仓库 `antonelli`
3. 点击 **"Uploading an existing file"**
4. 上传 `~/.openclaw/workspace/antonelli-full.zip`
5. 解压并提交

---

## 需要帮助？

如果在任何步骤遇到问题，请告诉我具体的错误信息。
