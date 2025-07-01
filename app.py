import os
import io
import json
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB最大文件大小

# 配置文件夹
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
MODEL_PATH = 'model/best.pt'

# 创建必要的文件夹
for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 全局变量存储模型
model = None

def load_model():
    """加载YOLOv8模型"""
    global model
    
    # 首先检查ultralytics是否正确安装
    try:
        import ultralytics
        logger.info(f"ultralytics版本: {ultralytics.__version__}")
    except ImportError as e:
        logger.error(f"ultralytics未正确安装: {str(e)}")
        logger.error("请运行: pip install --no-cache-dir ultralytics>=8.0.196")
        return False
    
    try:
        # 导入YOLOv8和torch
        import torch
        from ultralytics import YOLO
        
        # 解决PyTorch 2.6+ weights_only问题
        try:
            # 方法1: 添加安全全局类
            torch.serialization.add_safe_globals([
                'ultralytics.nn.tasks.DetectionModel',
                'ultralytics.nn.modules.block.C2f',
                'ultralytics.nn.modules.block.SPPF',
                'ultralytics.nn.modules.conv.Conv',
                'ultralytics.nn.modules.head.Detect',
                'collections.OrderedDict'
            ])
            logger.info("已添加PyTorch安全全局类")
        except Exception as e:
            logger.warning(f"添加安全全局类失败: {str(e)}")
            pass
        
        # 加载模型
        logger.info(f"正在加载模型: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
        logger.info(f"模型加载成功: {MODEL_PATH}")
        return True
        
    except ImportError as e:
        logger.error(f"模块导入失败: {str(e)}")
        if 'ultralytics.utils' in str(e):
            logger.error("ultralytics包损坏，请重新安装:")
            logger.error("pip uninstall ultralytics -y")
            logger.error("pip install --no-cache-dir ultralytics>=8.0.196")
        return False
        
    except Exception as e:
        logger.error(f"模型加载失败: {str(e)}")
        
        # 如果还是失败，尝试临时修改torch.load的默认行为
        try:
            import torch
            from ultralytics import YOLO
            
            logger.info("尝试使用兼容模式加载模型...")
            
            # 临时保存原始的load函数
            original_load = torch.load
            
            # 创建一个包装函数，设置weights_only=False
            def safe_load(*args, **kwargs):
                if 'weights_only' not in kwargs:
                    kwargs['weights_only'] = False
                return original_load(*args, **kwargs)
            
            # 临时替换torch.load
            torch.load = safe_load
            
            try:
                model = YOLO(MODEL_PATH)
                logger.info(f"模型加载成功 (使用兼容模式): {MODEL_PATH}")
                return True
            finally:
                # 恢复原始的load函数
                torch.load = original_load
                
        except ImportError as e2:
            logger.error(f"兼容模式导入失败: {str(e2)}")
            logger.error("建议运行修复脚本: python fix_torch_compatibility.py")
            return False
        except Exception as e2:
            logger.error(f"兼容模式加载也失败: {str(e2)}")
            logger.error("建议运行修复脚本: python fix_torch_compatibility.py")
            return False

def image_to_base64(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"图片转base64失败: {str(e)}")
        return None

def preprocess_image(image_path):
    """预处理图片"""
    try:
        # 使用PIL打开图片
        image = Image.open(image_path)
        # 转换为RGB模式（如果是RGBA等）
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        logger.error(f"图片预处理失败: {str(e)}")
        return None

def detect_objects(image_path):
    """使用YOLOv8进行目标检测"""
    global model
    try:
        if model is None:
            return None, "模型未加载"
        
        # 进行预测
        results = model(image_path)
        
        # 获取检测结果
        detections = []
        if results and len(results) > 0:
            result = results[0]
            boxes = result.boxes
            
            if boxes is not None:
                for i in range(len(boxes)):
                    box = boxes[i]
                    # 获取边界框坐标
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    # 获取置信度
                    confidence = float(box.conf[0])
                    # 获取类别
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id] if hasattr(model, 'names') else f"class_{class_id}"
                    
                    detection = {
                        'bbox': [x1, y1, x2, y2],
                        'confidence': confidence,
                        'class_id': class_id,
                        'class_name': class_name
                    }
                    detections.append(detection)
        
        # 保存结果图片
        result_image_path = None
        if results and len(results) > 0:
            annotated_img = results[0].plot()
            result_filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            result_image_path = os.path.join(RESULT_FOLDER, result_filename)
            cv2.imwrite(result_image_path, annotated_img)
        
        return {
            'detections': detections,
            'num_detections': len(detections),
            'result_image': result_image_path
        }, None
        
    except Exception as e:
        logger.error(f"目标检测失败: {str(e)}")
        return None, str(e)

@app.route('/')
def index():
    """主页"""
    # 获取浏览器语言偏好
    accepted_languages = request.headers.get('Accept-Language', '')
    
    # 简单的语言检测逻辑
    # 如果Accept-Language包含中文（zh、zh-CN、zh-TW等），使用中文版本
    # 否则使用英文版本
    if any(lang.strip().lower().startswith('zh') for lang in accepted_languages.split(',')):
        template = 'index.html'  # 中文版本
    else:
        template = 'index_en.html'  # 英文版本
    
    try:
        return render_template(template)
    except Exception as e:
        # 如果英文模板不存在，fallback到中文版本
        logger.warning(f"Template {template} not found, falling back to index.html: {str(e)}")
        return render_template('index.html')

@app.route('/en')
def index_en():
    """英文版主页"""
    return render_template('index_en.html')

@app.route('/zh')
def index_zh():
    """中文版主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """文件上传和识别接口"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件被上传'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            # 保存上传的文件
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # 预处理图片
            processed_image = preprocess_image(file_path)
            if processed_image is None:
                return jsonify({'error': '图片预处理失败'}), 400
            
            # 进行目标检测
            detection_result, error = detect_objects(file_path)
            if error:
                return jsonify({'error': f'检测失败: {error}'}), 500
            
            # 准备返回结果
            result = {
                'success': True,
                'filename': filename,
                'detections': detection_result['detections'],
                'num_detections': detection_result['num_detections'],
                'original_image': f'/uploads/{filename}'
            }
            
            # 如果有结果图片，添加到返回结果中
            if detection_result['result_image']:
                result_filename = os.path.basename(detection_result['result_image'])
                result['result_image'] = f'/results/{result_filename}'
            
            return jsonify(result)
        
        return jsonify({'error': '不支持的文件格式'}), 400
        
    except Exception as e:
        logger.error(f"上传处理失败: {str(e)}")
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/detect_url', methods=['POST'])
def detect_from_url():
    """从URL检测图片"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': '请提供图片URL'}), 400
        
        url = data['url']
        
        # 这里可以添加从URL下载图片的逻辑
        # 目前只是一个示例
        return jsonify({'error': 'URL检测功能正在开发中'}), 501
        
    except Exception as e:
        logger.error(f"URL检测失败: {str(e)}")
        return jsonify({'error': f'URL检测失败: {str(e)}'}), 500

@app.route('/model_info')
def model_info():
    """获取模型信息"""
    global model
    try:
        if model is None:
            return jsonify({'error': '模型未加载'}), 500
        
        info = {
            'model_loaded': True,
            'model_path': MODEL_PATH,
            'classes': model.names if hasattr(model, 'names') else {},
            'model_type': str(type(model).__name__)
        }
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"获取模型信息失败: {str(e)}")
        return jsonify({'error': f'获取模型信息失败: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """访问上传的文件"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def result_file(filename):
    """访问结果文件"""
    return send_from_directory(RESULT_FOLDER, filename)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': '文件太大，请上传小于16MB的文件'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 启动时加载模型
    print("正在加载YOLOv8模型...")
    if load_model():
        print("模型加载成功！")
        print(f"服务器启动在: http://localhost:5800")
        app.run(debug=True, host='0.0.0.0', port=5800)
    else:
        print("模型加载失败，请检查模型文件路径和依赖包") 