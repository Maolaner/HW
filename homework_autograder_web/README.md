# Homework Autograder Web App

## 简介
这是一个网页版的英语作业自动批改系统，支持上传图片或PDF作业文件，自动识别学生答案并对照标准答案进行批改。

## 使用方法
1. 安装依赖：
```
pip install -r requirements.txt
```

2. 安装 `poppler`（用于PDF识别）：
- macOS: `brew install poppler`

3. 运行程序：
```
python app.py
```

4. 在浏览器中打开：
```
http://127.0.0.1:5000/
```

上传作业后自动显示批改结果。
