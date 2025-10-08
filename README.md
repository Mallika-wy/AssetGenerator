# 项目简介
本项目旨在实现基于多模态输入（如多视角图片、单张图片+文字描述、视频等）的资产自动重建，最终生成可用于Isaac Sim的USD文件。该流程适用于数字孪生、虚拟仿真、机器人仿真等场景。

## 支持的输入类型
- 多视角图片
- 单张图片 + 文字描述
- 视频（可自动抽帧为图片）

## 主要流程
1. **数据采集与预处理**
   - 视频自动抽帧为图片（`video2images.py`）
   - 图片归档与整理
2. **3D重建（多视角图片）**
   - 使用COLMAP进行相机位姿估计与稠密点云重建
   - 点云后处理（滤波、裁剪等）
3. **3D模型生成**
   - 点云转网格（如Poisson重建、Open3D等工具）
   - 网格简化与修复
4. **USD文件构建**
   - 将3D网格、纹理等信息导出为USD格式，便于在Isaac Sim等平台使用

## 技术路线
- 多视角图片：COLMAP → 点云 → 网格 → USD
- 单张图片+描述：可探索基于生成式AI的3D重建（如DreamFusion、LGM等，后续可扩展）
- 视频：先抽帧为图片，流程同多视角图片

## 依赖环境
- Python 3.8+
- OpenCV（视频抽帧）
- COLMAP（3D重建，需单独安装）
- Open3D 或 MeshLab（点云转网格）
- NVIDIA Omniverse/Isaac Sim（USD文件查看与仿真）

## 使用方法
1. 视频转图片：
   ```bash
   python video2images.py <video_path> <output_images_dir> <frames_per_second>
   ```
2. 多视角图片3D重建：
   - 使用COLMAP命令行或GUI进行特征提取、匹配、稀疏/稠密重建
   - 导出点云/网格
3. 网格处理与USD导出：
   - 使用Open3D等工具处理网格
   - 导出为USD文件

## 参考资料
- [COLMAP官方文档](https://colmap.github.io/)
- [Open3D官方文档](http://www.open3d.org/)
- [NVIDIA Omniverse USD介绍](https://docs.omniverse.nvidia.com/)

---
如需扩展单图+文本描述的3D重建，可关注近期的生成式AI 3D建模前沿进展。