# Android 打包指南（Kivy + Buildozer）

本仓库已保留 Android 打包所需的最小工程：`output/android_app/`。

目标：在一台干净的 Linux/WSL/Docker 环境中，生成可安装到安卓手机的 APK。

## 算法原理

本项目内置两种可逆的文本“加/解密”方式，均支持中文：

- Unicode 码位移（+3/-3）
  - 思路：将明文中每个字符的 Unicode 码点加 3，得到密文；解密时每个字符减 3 还原。
  - 形式化：设明文字符为 \(c\)，其码点为 \(code(c)\)，则
    - 加密：\(c' = chr(code(c)+3)\)
    - 解密：\(c = chr(code(c')-3)\)
  - 示例：
    - "abc" → "def"
    - "你好" → "呜咍"
  - 特性：实现简单、可逆、对 Unicode 友好；但安全性较弱，不适合保护敏感信息，仅作轻量私密或演示用途。

- Base64 编解码
  - 思路：将文本按 UTF-8 编码为字节序列，再用 Base64 进行编码；解密时反向解码并按 UTF-8 还原文本。
  - 示例：
    - "abc" → "YWJj"
    - "你好" → "5L2g5aW9"
  - 特性：广泛兼容、可逆、非加密而是“文本传输编码”。任何标准 Base64 工具均可还原。

伪代码（Python）：

```python
# Unicode 码位移
def encrypt_unicode_shift(text):
    return "".join(chr(ord(ch)+3) for ch in text)

def decrypt_unicode_shift(text):
    return "".join(chr(ord(ch)-3) for ch in text)

# Base64（UTF-8）
import base64
def encrypt_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt_base64(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')
```

## 目录

```
output/
  android_app/
    main.py            # Kivy 程序入口，已复用 crypto 算法
    buildozer.spec     # Buildozer 打包配置
    crypto/            # 与桌面端一致的算法模块
    assets/            # 应用图标等资源（可自行放置 icon.png）
```

## 环境准备

1. 系统要求：Ubuntu 20.04+/Debian/WSL2（推荐 Ubuntu），或使用 Docker 容器
2. 安装系统依赖：
```bash
sudo apt-get update
sudo apt-get install -y build-essential git python3 python3-dev \ 
    libffi-dev libssl-dev libsqlite3-dev zlib1g-dev openjdk-17-jdk unzip zip
```
3. 安装 Python 包：
```bash
python3 -m pip install --upgrade pip
python3 -m pip install buildozer Cython
```

## 打包步骤

1. 进入工程目录：
```bash
cd output/android_app
```
2. 初始化（已提供 buildozer.spec，可跳过）：
```bash
buildozer init
```
3. 构建 APK（调试版）：
```bash
buildozer android debug
```
首轮会自动下载 Android SDK/NDK，耗时较长。完成后 APK 位于：
```
output/android_app/bin/*.apk
```

4. 安装到设备（连接 USB 且已开启调试）：
```bash
buildozer android deploy run
```

## 自定义与常见问题

- 修改应用图标：把图标放入 `output/android_app/assets/icon.png`，并在 `buildozer.spec` 中设置：
  ```
  icon.filename = assets/icon.png
  ```
- 更改包名/版本：在 `buildozer.spec` 的 `[app]` 段编辑：
  ```
  title = Encryption Tool
  package.name = encryptiontool
  package.domain = org.example
  version = 0.1
  ```
- 权限：如需网络/存储等权限，在 `buildozer.spec` 中追加：
  ```
  android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
  ```
- 首次编译失败：执行 `buildozer android clean` 后重试；或删除 `.buildozer/` 目录后再编译。
- 兼容架构：默认 `arm64-v8a, armeabi-v7a`，如需仅 64 位可在 `buildozer.spec` 修改：
  ```
  android.archs = arm64-v8a
  ```

## 说明

- Android 端 UI 使用 Kivy 重写以保证稳定打包；算法模块与桌面版一致，功能与交互（点击头像展开/收起、拖拽移动、位置记忆）保持一致。
- 若需发布签名版：
  ```bash
  buildozer android release
  # 按提示完成签名与对齐
  ```

完成以上步骤后，你即可在安卓设备上安装并稳定运行本应用。 

## Windows 打包指南（PyInstaller）

以下命令在 Windows PowerShell 下执行，建议使用虚拟环境，确保可复制与干净依赖。

1. 创建并启用虚拟环境（项目根目录）：
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install PyQt5==5.15.11 pyinstaller
```

2. 生成“文件夹版”可执行程序（启动更快，推荐分发整个文件夹）：
```powershell
.\.venv\Scripts\pyinstaller --noconfirm --clean --windowed `
  --name EncryptionTool `
  --icon ui/resources/ico.ico `
  --add-data "ui/resources;ui/resources" `
  --add-data "crypto;crypto" `
  --collect-all PyQt5 `
  main.py
```
产物位置：`dist/EncryptionTool/EncryptionTool.exe`（连同同级文件夹整体拷贝即可开箱即用）。

3. 生成“单文件版”可执行程序（单一 exe，首次启动有自解压时延）：
```powershell
.\.venv\Scripts\pyinstaller --noconfirm --clean --onefile --windowed `
  --name EncryptionTool-onefile `
  --icon ui/resources/ico.ico `
  --add-data "ui/resources;ui/resources" `
  --add-data "crypto;crypto" `
  --collect-all PyQt5 `
  main.py
```
产物位置：`dist/EncryptionTool-onefile.exe`。

4. 常见问题
- 若运行时提示缺少 Qt/PyQt5 组件，务必使用上面的 `--collect-all PyQt5` 参数，或改为：
  `--collect-submodules PyQt5 --collect-data PyQt5 --collect-binaries PyQt5`。
- 图标与资源需通过 `--add-data` 一并打包，Windows 下分隔符用分号 `;`。
- 高分屏模糊可在创建 `QApplication` 前添加：
  ```python
  from PyQt5.QtCore import Qt
  from PyQt5.QtWidgets import QApplication
  QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
  QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
  ```