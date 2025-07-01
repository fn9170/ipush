#!/bin/bash

# YOLOv8 目标识别系统 Docker 部署脚本
# 适用于 x86 架构

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_NAME="yolov8-detection"
IMAGE_NAME="yolov8-detection-app"
CONTAINER_NAME="yolov8-detection-app"
PORT="5800"

# 打印彩色消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_step "检查系统依赖..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_warning "docker-compose 未安装，将使用 docker build 方式"
        USE_COMPOSE=false
    else
        USE_COMPOSE=true
    fi
    
    print_message "依赖检查完成"
}

# 检查模型文件
check_model() {
    print_step "检查模型文件..."
    
    if [ ! -f "model/best.pt" ]; then
        print_error "模型文件 model/best.pt 不存在！"
        print_message "请确保模型文件位于 model/best.pt"
        exit 1
    fi
    
    print_message "模型文件检查完成"
}

# 创建必要目录
create_directories() {
    print_step "创建必要目录..."
    
    mkdir -p uploads results logs
    
    # 创建 .gitkeep 文件保持目录结构
    touch uploads/.gitkeep results/.gitkeep logs/.gitkeep
    
    print_message "目录创建完成"
}

# 停止并删除现有容器
cleanup_containers() {
    print_step "清理现有容器..."
    
    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        print_message "停止现有容器..."
        docker stop $CONTAINER_NAME || true
        docker rm $CONTAINER_NAME || true
    fi
    
    print_message "容器清理完成"
}

# 构建 Docker 镜像
build_image() {
    print_step "构建 Docker 镜像..."
    
    if [ "$USE_COMPOSE" = true ]; then
        print_message "使用 docker-compose 构建..."
        docker-compose build --no-cache
    else
        print_message "使用 docker build 构建..."
        docker build -t $IMAGE_NAME . --no-cache
    fi
    
    print_message "镜像构建完成"
}

# 启动容器
start_container() {
    print_step "启动容器..."
    
    if [ "$USE_COMPOSE" = true ]; then
        print_message "使用 docker-compose 启动..."
        docker-compose up -d
    else
        print_message "使用 docker run 启动..."
        docker run -d \
            --name $CONTAINER_NAME \
            -p $PORT:$PORT \
            -v $(pwd)/uploads:/app/uploads \
            -v $(pwd)/results:/app/results \
            -v $(pwd)/logs:/app/logs \
            --restart unless-stopped \
            $IMAGE_NAME
    fi
    
    print_message "容器启动完成"
}

# 等待服务就绪
wait_for_service() {
    print_step "等待服务启动..."
    
    echo -n "等待服务就绪"
    for i in {1..30}; do
        if curl -s http://localhost:$PORT/model_info > /dev/null 2>&1; then
            echo ""
            print_message "服务已就绪！"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    echo ""
    print_warning "服务启动超时，请检查日志"
}

# 显示状态信息
show_status() {
    print_step "显示部署状态..."
    
    echo ""
    echo "🎉 部署完成！"
    echo ""
    echo "📊 服务信息："
    echo "   - 应用地址: http://localhost:$PORT"
    echo "   - 容器名称: $CONTAINER_NAME"
    echo "   - 镜像名称: $IMAGE_NAME"
    echo ""
    echo "🔧 管理命令："
    echo "   - 查看日志: docker logs $CONTAINER_NAME"
    echo "   - 停止服务: docker stop $CONTAINER_NAME"
    echo "   - 重启服务: docker restart $CONTAINER_NAME"
    if [ "$USE_COMPOSE" = true ]; then
        echo "   - 使用 Compose 停止: docker-compose down"
        echo "   - 使用 Compose 重启: docker-compose restart"
    fi
    echo ""
}

# 主函数
main() {
    echo "🚀 YOLOv8 目标识别系统 Docker 部署脚本"
    echo "=================================="
    echo ""
    
    check_dependencies
    check_model
    create_directories
    cleanup_containers
    build_image
    start_container
    wait_for_service
    show_status
    
    print_message "部署脚本执行完成！"
}

# 命令行参数处理
case "${1:-}" in
    "build")
        check_dependencies
        check_model
        build_image
        ;;
    "start")
        start_container
        wait_for_service
        ;;
    "stop")
        if [ "$USE_COMPOSE" = true ]; then
            docker-compose down
        else
            docker stop $CONTAINER_NAME
        fi
        ;;
    "restart")
        if [ "$USE_COMPOSE" = true ]; then
            docker-compose restart
        else
            docker restart $CONTAINER_NAME
        fi
        ;;
    "logs")
        docker logs -f $CONTAINER_NAME
        ;;
    "clean")
        cleanup_containers
        docker rmi $IMAGE_NAME 2>/dev/null || true
        print_message "清理完成"
        ;;
    "help"|"-h"|"--help")
        echo "用法: $0 [命令]"
        echo ""
        echo "命令:"
        echo "  (无参数)  - 完整部署流程"
        echo "  build     - 只构建镜像"
        echo "  start     - 只启动容器"
        echo "  stop      - 停止容器"
        echo "  restart   - 重启容器"
        echo "  logs      - 查看日志"
        echo "  clean     - 清理容器和镜像"
        echo "  help      - 显示帮助信息"
        ;;
    "")
        main
        ;;
    *)
        print_error "未知命令: $1"
        echo "使用 '$0 help' 查看帮助信息"
        exit 1
        ;;
esac 