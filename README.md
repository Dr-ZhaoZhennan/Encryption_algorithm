# 豆包风格浮动加密助手

## 项目简介

本项目是一个 Windows 下的桌面悬浮加密助手，界面风格类似豆包，支持如下特性：

- 悬浮头像，鼠标移入弹出加密面板，支持拖动、右键退出。
- 支持两种稳定、可逆的加密算法：
  - **Unicode码位移（支持中文）**：每个字符的Unicode码+3，解密时-3。
  - **Base64（支持中文）**：标准Base64编码/解码。
- 输入框支持中英文混合文本。
- 操作按钮：加密、解密、复制、清空。
- 解密原理详细说明，便于手动还原。
- 程序记忆上次关闭时的位置。
- 资源占用低，界面响应迅速。

## 依赖环境

- Python 3.7 及以上
- PyQt5
- PyInstaller（仅打包时需要）

安装依赖：
```bash
pip install PyQt5
pip install pyinstaller
```

## 运行方式

1. 确保 `ui/resources/photo.png` 头像图片存在。
2. 在命令行进入项目目录：
   ```bash
   cd /E:/Desktop/translate_AI
   ```
3. 运行主程序：
   ```bash
   python main.py
   ```

## 打包为exe

1. 确保已安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```
2. 准备图标文件 `ui/resources/ico.ico`（建议 256x256 像素）。
3. 在命令行执行打包命令：
   ```bash
   pyinstaller --noconsole --onefile --icon=ui/resources/ico.ico --add-data "ui/resources/photo.png;ui/resources" main.py
   ```
   - `--noconsole`：不弹出命令行窗口。
   - `--onefile`：生成单一exe文件。
   - `--icon`：指定exe图标。
   - `--add-data`：打包头像图片。

4. 打包完成后，`dist/main.exe` 即为可执行文件。

## 注意事项

- 如需打包其它资源，可多次使用 `--add-data`。
- 若资源路径有问题，建议在代码中用如下方式获取兼容路径：
  ```python
  import sys, os
  if getattr(sys, 'frozen', False):
      base_path = sys._MEIPASS
  else:
      base_path = os.path.dirname(__file__)
  avatar_path = os.path.join(base_path, 'ui', 'resources', 'photo.png')
  ```
- 若杀毒软件误报，属正常现象。

## 目录结构

```
translate_AI/
├─ main.py
├─ requirements.txt
├─ README.md
├─ crypto/
│    ├─ __init__.py
│    ├─ unicode_shift.py
│    └─ base64_codec.py
├─ ui/
│    ├─ floating_avatar.py
│    └─ resources/
│         ├─ photo.png
│         └─ ico.ico
```

---
如有问题或建议，欢迎反馈！ 