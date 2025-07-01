# YOLO Inspector

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

### 3. 支持的格式
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

## 项目结构

```
vision-detect-check/
├── app.py              # Flask主应用
├── requirements.txt    # 依赖包列表
├── README.md          # 中文项目说明
├── README_EN.md       # 英文项目说明
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

## 故障排除

### 常见问题

1. **ultralytics.utils 模块错误**
   
   **问题**: 看到 "No module named 'ultralytics.utils'" 或类似错误
   
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
   
   **问题**: 如果您看到类似 "Weights only load failed" 或 "WeightsUnpickler error" 的错误信息，这是PyTorch 2.6+版本的兼容性问题。
   
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
   
   **方法3**: 代码已自动修复
   - 最新的app.py已包含兼容性修复代码
   - 直接运行应用即可

 3. **其他模型加载问题**
   - 检查 `model/best.pt` 文件是否存在
   - 确认ultralytics包安装正确
   - 检查Python版本兼容性

2. **依赖包安装失败**
   - 升级pip: `pip install --upgrade pip`
   - 使用镜像源: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

3. **GPU相关问题**
   - CPU模式: 自动使用CPU进行推理
   - GPU模式: 确保CUDA环境配置正确

4. **端口占用**
   - 修改app.py中的端口号: `app.run(port=5801)`

### 性能优化

1. **GPU加速**
   ```bash
   # 安装GPU版本PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **模型优化**
   - 使用TensorRT优化模型
   - 转换为ONNX格式提升推理速度

## 开发说明

### 扩展功能
- 添加视频文件识别支持
- 集成更多预训练模型
- 添加用户认证系统
- 实现识别结果数据库存储

### 代码结构
- `load_model()`: 模型加载函数
- `detect_objects()`: 目标检测核心函数
- `upload_file()`: 文件上传处理路由
- `model_info()`: 模型信息查询路由

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 支持

如遇问题或建议，请通过以下方式联系:
- 创建Issue报告问题
- 提交Pull Request贡献代码
- 发送邮件询问技术问题

---

**注意**: 请确保您有权使用提供的YOLOv8模型文件，并遵守相关的许可证要求。

---

# English

An intelligent object detection platform based on Flask and YOLOv8, providing a clean and beautiful user interface with powerful AI recognition capabilities.

## Features

- 🎯 **Smart Detection**: High-precision object detection based on YOLOv8 model
- 🌐 **Web Interface**: Modern responsive user interface  
- 🌍 **Multi-language**: Automatic language detection (Chinese/English)
- 📁 **Drag & Drop**: Support drag-and-drop files and click upload
- 📊 **Results Display**: Real-time display of detection results and confidence statistics
- 🖼️ **Visualization**: Comparative display of original and annotated result images
- 🔍 **Image Zoom**: Click to enlarge images for detailed viewing
- 📱 **Mobile Friendly**: Support for mobile and tablet device access

## Interface Preview

![YOLO Inspector Screenshot](ui/page.png)

*YOLO Inspector main interface showcasing modern design and intuitive operation workflow*

### Interface Features
- **Left Operation Panel**: Model selection, image upload, language switching
- **Right Results Display**: Side-by-side comparison of original and detection results
- **Smart Statistics Cards**: Detected objects count, max confidence, average confidence
- **Detailed Detection List**: Shows all detected object categories and confidence scores
- **Image Zoom Function**: Click images to view full-screen high-resolution details
- **Responsive Design**: Optimized for both desktop and mobile devices

## System Requirements

- Python 3.8+
- 8GB+ RAM recommended
- GPU support (optional but recommended)

## Installation Guide

### 1. Clone and enter project directory

```bash
cd radar-vision-identify-ai/vision-detect-check
```

### 2. Create virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify model file

Ensure the `model/best.pt` file exists and is accessible. This is the trained YOLOv8 model file.

## Quick Start

### ⚡ If you encounter "ultralytics.utils" error

**Fastest solution**:
```bash
python quick_fix.py
```

### 📋 If you encounter model loading issues (PyTorch 2.6+)

**Complete fix script**:
```bash
python fix_torch_compatibility.py
```

### Start server

**Method 1**: Use smart startup script (recommended)
```bash
python run.py
```

**Method 2**: Direct startup
```bash
python app.py
```

### Access application

Open browser and visit: `http://localhost:5800`

## Usage Instructions

### 1. Upload Image
- Method 1: Click "Select Image" button to choose file
- Method 2: Directly drag image files to upload area

### 2. View Results
- System automatically processes uploaded images
- Displays comparison between original and detection result images
- Shows statistics like number of detected objects, confidence levels
- Lists all detected object categories and confidence scores

### 3. Language Switching
- System automatically detects browser language
- Manual switching via language buttons in top-right corner
- Direct access: `/en` for English, `/zh` for Chinese

### 4. Supported Formats
- Image formats: JPG, PNG, GIF, BMP, TIFF
- File size: Maximum 16MB

## API Endpoints

### File Upload Recognition
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: Image file

Response:
{
    "success": true,
    "filename": "uploaded_filename",
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

### Get Model Information
```
GET /model_info

Response:
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

### Language-specific Routes
```
GET /          # Auto-detect language
GET /en        # Force English
GET /zh        # Force Chinese
```

## Project Structure

```
vision-detect-check/
├── app.py                    # Flask main application
├── requirements.txt          # Dependencies list
├── README.md                # Project documentation
├── run.py                   # Smart startup script
├── model/                   # Model files directory
│   └── best.pt             # YOLOv8 model file
├── templates/              # HTML templates
│   ├── index.html          # Chinese homepage template
│   └── index_en.html       # English homepage template
├── ui/                     # Interface screenshots
│   └── page.png            # Main interface screenshot
├── uploads/                # Upload storage (auto-created)
├── results/                # Result images storage (auto-created)
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── deploy.sh              # Deployment script
```

## Configuration

### Model Configuration
- Model path: `model/best.pt`
- Supported formats: PyTorch (.pt), ONNX (.onnx)

### Server Configuration
- Default port: 5800
- Maximum file size: 16MB
- Debug mode: Enabled by default in development

### Modify Configuration
You can modify the following configurations in `app.py`:

```python
# File size limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Model path
MODEL_PATH = 'model/best.pt'

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
```

## Docker Deployment

### Build and run with Docker

```bash
# Build image
docker build -t yolo-inspector .

# Run container
docker run -p 5800:5800 yolo-inspector
```

### Use Docker Compose

```bash
# Start service
docker-compose up -d

# Stop service  
docker-compose down
```

### Use deployment script

```bash
# Make executable
chmod +x deploy.sh

# Deploy
./deploy.sh build
./deploy.sh start
```

## Troubleshooting

### Common Issues

1. **ultralytics.utils module error**
   
   **Problem**: See "No module named 'ultralytics.utils'" or similar errors
   
   **Solution**:
   
   **Quick fix** (recommended):
   ```bash
   python quick_fix.py
   ```
   
   **Manual fix**:
   ```bash
   pip uninstall ultralytics -y
   pip install --no-cache-dir ultralytics>=8.0.196
   ```

2. **Model loading failure (PyTorch 2.6+ compatibility issues)**
   
   **Problem**: If you see errors like "Weights only load failed" or "WeightsUnpickler error", this is a PyTorch 2.6+ compatibility issue.
   
   **Solution**:
   
   **Method 1**: Use complete fix script (recommended)
   ```bash
   python fix_torch_compatibility.py
   ```
   
   **Method 2**: Manual PyTorch downgrade
   ```bash
   pip uninstall torch torchvision -y
   pip install "torch>=2.0.0,<2.6.0" "torchvision>=0.15.0,<0.20.0"
   ```
   
   **Method 3**: Code auto-fix included
   - Latest app.py includes compatibility fix code
   - Run application directly

3. **Other model loading issues**
   - Check if `model/best.pt` file exists
   - Confirm ultralytics package is installed correctly
   - Check Python version compatibility

4. **Dependency installation failure**
   - Upgrade pip: `pip install --upgrade pip`
   - Use mirror source: `pip install -r requirements.txt -i https://pypi.douban.com/simple/`

5. **GPU related issues**
   - CPU mode: Automatically uses CPU for inference
   - GPU mode: Ensure CUDA environment is configured correctly

6. **Port occupied**
   - Modify port number in app.py: `app.run(port=5801)`

### Performance Optimization

1. **GPU Acceleration**
   ```bash
   # Install GPU version PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Model Optimization**
   - Use TensorRT to optimize model
   - Convert to ONNX format to improve inference speed

## Development

### Extended Features
- Add video file recognition support
- Integrate more pre-trained models
- Add user authentication system
- Implement recognition result database storage

### Code Structure
- `load_model()`: Model loading function
- `detect_objects()`: Core object detection function
- `upload_file()`: File upload processing route
- `model_info()`: Model information query route
- Language detection and routing logic

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

If you encounter issues or have suggestions, please contact us through:
- Create an Issue to report problems
- Submit a Pull Request to contribute code
- Send email for technical questions

---

**Note**: Please ensure you have the right to use the provided YOLOv8 model files and comply with relevant license requirements.