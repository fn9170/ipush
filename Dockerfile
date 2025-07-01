# 使用官方Python 3.9运行时作为基础镜像 (适合x86架构)
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖 (OpenCV和其他库需要)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libgtk-3-0 \
    python3-opencv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 首先复制requirements.txt以利用Docker缓存
COPY requirements.txt .

# 升级pip并安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p uploads results logs

# 设置目录权限
RUN chmod -R 755 /app

# 暴露应用端口
EXPOSE 5800

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5800/model_info || exit 1

# 启动命令
CMD ["python", "app.py"] 