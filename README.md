# AI 智能重复照片清理工具

🚀 基于感知哈希算法的智能重复图片清理工具，快速识别并清理重复/相似照片，释放存储空间。

## 功能特点
- ✅ **高精度识别**：使用dHash感知哈希算法，支持完全相同和相似图片检测
- ✅ **安全删除**：删除的文件自动移到回收站，避免误删无法恢复
- ✅ **批量处理**：支持一键扫描整个目录下所有图片
- ✅ **自定义阈值**：可调整相似度阈值，满足不同场景需求
- ✅ **报告导出**：自动生成重复图片报告，方便预览核对
- ✅ **跨平台**：支持 macOS / Windows / Linux

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法
### 1. 仅扫描生成报告（不删除）
```bash
python main.py /path/to/your/photos --report-only
```
执行后会生成 `duplicates_report.json` 报告文件，包含所有重复图片信息。

### 2. 扫描并清理重复图片
```bash
python main.py /path/to/your/photos
```
扫描完成后会提示确认删除，确认后自动删除重复文件（保留最新版本）。

### 3. 自定义参数
```bash
# 保留最旧的图片
python main.py /path/to/your/photos --keep oldest

# 调整相似度阈值，识别相似图片（阈值越大，匹配越宽松）
python main.py /path/to/your/photos --threshold 5

# 指定报告输出路径
python main.py /path/to/your/photos --output my_report.json
```

## 支持的图片格式
- JPG/JPEG
- PNG
- GIF
- BMP
- WebP

## 注意事项
1. 首次使用建议先加 `--report-only` 参数生成报告，确认无误后再执行删除
2. 大数量图片扫描时请耐心等待，速度取决于图片数量和大小
3. 删除的文件会保存在系统回收站，可随时恢复

## 许可证
MIT License
