# YOLO Inspector

[English](README.md) | [中文](README_ZH.md)

---

基于Flask和YOLOv8的智能目标检测平台，提供简洁美观的用户界面和强大的AI识别功能。

## 功能特性

- 🎯 **智能识别**: 基于YOLOv8模型进行高精度目标检测
- 🌐 **Web界面**: 现代化响应式用户界面
- 🌍 **多语言支持**: 自动检测浏览器语言，支持中英文切换
- 📁 **拖拽上传**: 支持拖拽文件和点击上传
- 📊 **结果展示**: 实时显示检测结果和置信度统计
- 🖼️ **可视化**: 对比显示原图和标注结果图
- 🔍 **图片放大**: 点击图片可放大查看详细内容
- 📱 **移动友好**: 支持手机和平板设备访问

## 界面预览

![YOLO Inspector 界面截图](ui/page.png)

*YOLO Inspector 主界面展示了现代化的设计和直观的操作流程*

### 界面特色
- **左侧操作面板**: 模型选择、图片上传、语言切换等功能
- **右侧结果展示**: 原图与检测结果对比展示
- **智能统计卡片**: 检测目标数量、最高置信度、平均置信度
- **详细检测列表**: 展示所有检测到的目标类别和置信度
- **图片缩放功能**: 点击图片可全屏查看高清细节
- **响应式设计**: 适配桌面端和移动端设备

## 系统要求

- Python 3.8+
- 8GB+ 内存推荐
- GPU支持（可选，但推荐）

## 安装指南

### 1. 克隆并进入项目目录

```bash
cd radar-vision-identify-ai/vision-detect-check
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证模型文件

确保 `model/best.pt` 文件存在且可访问。这是训练好的YOLOv8模型文件。

## 快速开始

### ⚡ 如果遇到 "ultralytics.utils" 错误

**最快解决方案**:
```bash
python quick_fix.py
```

### 📋 如果遇到模型加载问题 (PyTorch 2.6+)

**完整修复脚本**:
```bash
python fix_torch_compatibility.py
```

### 启动服务器

**方法1**: 使用智能启动脚本 (推荐)
```bash
python run.py
```

**方法2**: 直接启动
```bash
python app.py
```

### 访问应用

打开浏览器访问: `http://localhost:5800`

## 使用说明

### 1. 上传图片
- 方法一：点击"选择图片"按钮选择文件
- 方法二：直接拖拽图片文件到上传区域

### 2. 查看结果
- 系统会自动处理上传的图片
- 显示原始图片和检测结果对比
- 展示检测到的目标数量、置信度等统计信息
- 列出所有检测到的目标类别和置信度

### 3. 语言切换
- 系统自动检测浏览器语言
- 可通过右上角语言按钮手动切换
- 直接访问：`/en`（英文）、`/zh`（中文）

### 4. 支持的格式
- 图片格式：JPG, PNG, GIF, BMP, TIFF
- 文件大小：最大16MB

## API接口

### 文件上传识别
```
POST /upload
Content-Type: multipart/form-data

参数:
- file: 图片文件

返回:
{
    "success": true,
    "filename": "上传的文件名",
    "detections": [
        {
            "bbox": [x1, y1, x2, y2],
            "confidence": 0.95,
            "class_id": 0,
            "class_name": "person"
        }
    ],
    "num_detections": 1,
    "original_image": "/uploads/filename.jpg",
    "result_image": "/results/result_filename.jpg"
}
```

### 获取模型信息
```
GET /model_info

返回:
{
    "model_loaded": true,
    "model_path": "model/best.pt",
    "classes": {
        "0": "person",
        "1": "car",
        ...
    },
    "model_type": "YOLO"
}
```

### 语言特定路由
```
GET /          # 自动检测语言
GET /en        # 强制英文
GET /zh        # 强制中文
```

## 项目结构

```
vision-detect-check/
├── app.py              # Flask主应用
├── requirements.txt    # 依赖包列表
├── README.md          # 英文项目说明（默认）
├── README_ZH.md       # 中文项目说明
├── run.py             # 智能启动脚本
├── model/             # 模型文件目录
│   └── best.pt        # YOLOv8模型文件
├── templates/         # HTML模板
│   ├── index.html     # 中文主页模板
│   └── index_en.html  # 英文主页模板
├── ui/                # 界面截图
│   └── page.png       # 主界面截图
├── uploads/           # 上传文件存储（自动创建）
├── results/           # 结果图片存储（自动创建）
├── Dockerfile         # Docker配置文件
├── docker-compose.yml # Docker Compose配置
└── deploy.sh          # 部署脚本
```

## 配置说明

### 模型配置
- 模型路径: `model/best.pt`
- 支持的模型格式: PyTorch (.pt), ONNX (.onnx)

### 服务器配置
- 默认端口: 5800
- 最大文件大小: 16MB
- 调试模式: 开发环境默认开启

### 修改配置
在 `app.py` 中可以修改以下配置:

```python
# 文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 模型路径
MODEL_PATH = 'model/best.pt'

# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
```

## Docker部署

### 使用Docker构建和运行

```bash
# 构建镜像
docker build -t yolo-inspector .

# 运行容器
docker run -p 5800:5800 yolo-inspector
```

### 使用Docker Compose

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down
```

### 使用部署脚本

```bash
# 赋予执行权限
chmod +x deploy.sh

# 部署
./deploy.sh build
./deploy.sh start
```

## 故障排除

### 常见问题

1. **ultralytics.utils 模块错误**
   
   **问题**: 出现 "No module named 'ultralytics.utils'" 或类似错误
   
   **解决方案**:
   
   **快速修复** (推荐):
   ```bash
   python quick_fix.py
   ```
   
   **手动修复**:
   ```bash
   pip uninstall ultralytics -y
   pip install --no-cache-dir ultralytics>=8.0.196
   ```

2. **模型加载失败 (PyTorch 2.6+ 兼容性问题)**
   
   **问题**: 如果您看到类似 "Weights only load failed" 或 "WeightsUnpickler error" 的错误，这是 PyTorch 2.6+ 的兼容性问题。
   
   **解决方案**:
   
   **方法1**: 使用完整修复脚本 (推荐)
   ```bash
   python fix_torch_compatibility.py
   ```
   
   **方法2**: 手动降级PyTorch
   ```bash
   pip uninstall torch torchvision -y
   pip install "torch>=2.0.0,<2.6.0" "torchvision>=0.15.0,<0.20.0"
   ```
   
   **方法3**: 代码自动修复已包含
   - 最新的 app.py 包含兼容性修复代码
   - 直接运行应用程序即可

3. **其他模型加载问题**
   - 检查 `model/best.pt` 文件是否存在
   - 确认 ultralytics 包已正确安装
   - 检查 Python 版本兼容性

4. **依赖安装失败**
   - 升级pip: `pip install --upgrade pip`
   - 使用镜像源: `pip install -r requirements.txt -i https://pypi.douban.com/simple/`

5. **GPU相关问题**
   - CPU模式: 自动使用CPU进行推理
   - GPU模式: 确保CUDA环境配置正确

6. **端口被占用**
   - 修改app.py中的端口号: `app.run(port=5801)`

### 性能优化

1. **GPU加速**
   ```bash
   # 安装GPU版本PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **模型优化**
   - 使用TensorRT优化模型
   - 转换为ONNX格式提高推理速度

## 开发

### 扩展功能
- 添加视频文件识别支持
- 集成更多预训练模型
- 添加用户认证系统
- 实现识别结果数据库存储

### 代码结构
- `load_model()`: 模型加载函数
- `detect_objects()`: 核心目标检测函数
- `upload_file()`: 文件上传处理路由
- `model_info()`: 模型信息查询路由
- 语言检测和路由逻辑

### 贡献代码
1. Fork本仓库
2. 创建功能分支
3. 进行您的修改
4. 如果适用，添加测试
5. 提交Pull Request

## 许可证

本项目基于MIT许可证。详情请参阅LICENSE文件。

## 支持

如果遇到问题或有建议，请通过以下方式联系我们：
- 创建Issue反馈问题
- 提交Pull Request贡献代码
- 发送邮件询问技术问题

---

**注意**: 请确保您有权使用提供的YOLOv8模型文件，并遵守相关的许可证要求。 