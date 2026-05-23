# Railway/Render 部署指南

## 方案一：Railway 部署（推荐）

### 1. 创建 Railway 项目
1. 访问 [railway.app](https://railway.app)，登录GitHub账号
2. 点击 **New Project** → **Deploy from GitHub repo**
3. 选择你的仓库

### 2. 配置环境变量
在 Railway 控制台添加以下环境变量：
```
PYTHONPATH = .
```

### 3. 设置启动命令
在 Railway 控制台的 **Start Command** 填写：
```
gunicorn -w 1 -b :$PORT wsgi:app --timeout 300
```

### 4. 添加依赖
Railway会自动检测 `requirements.txt`

---

## 方案二：Render 部署

### 1. 创建 Render 账号
访问 [render.com](https://render.com)，连接GitHub仓库

### 2. 创建 Web Service
- **Name**: `方案生成器`
- **Region**: Singapore（东南亚访问快）
- **Branch**: main
- **Root Directory**: （留空）
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 1 -b :$PORT wsgi:app --timeout 300`

### 3. 添加环境变量
同Railway配置

### 4. 启用持久化磁盘（可选）
如果需要保存上传的文件和生成的文档，可以在 **Disk** 设置中添加存储卷。

---

## 本地测试

部署前先在本地测试：
```bash
pip install gunicorn
gunicorn -w 1 -b :5000 wsgi:app
```

访问 http://localhost:5000

---

## 注意事项

1. **Excel文件**: 确保 `厚溥国际职业教育国际化产品报价单2026版(2.0).xlsx` 在项目根目录
2. **上传文件**: 需要持久化存储，Railway/Render都需要配置磁盘存储
3. **文件上传限制**: Vercel Functions限制100KB，Railway/Render更宽松

---

## 下一步

需要我帮你创建 `gunicorn.conf.py` 配置文件吗？或者直接开始部署？