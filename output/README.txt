Windows 打包结果
- 目录: output/windows/EncryptionTool
- 运行: 双击 EncryptionTool.exe 即可，无需安装 Python。

Android 打包说明（需在 Linux/WSL/Docker 环境执行）
- 工程骨架: output/android_app
- 步骤（在 output/android_app 下）：
  1) 安装依赖: pip install buildozer Cython
  2) 安装系统依赖: sudo apt-get update && sudo apt-get install -y build-essential git python3-dev libffi-dev libssl-dev libsqlite3-dev zlib1g-dev openjdk-17-jdk
  3) 初始化(已提供 spec 可跳过): buildozer init
  4) 构建 APK: buildozer android debug
  5) 生成的 APK 路径: output/android_app/bin/*.apk

说明
- Android 版本采用 Kivy 重写 UI（保留相同加/解密算法逻辑），确保在安卓上稳定运行。
- 若需发布签名版，执行: buildozer android release && buildozer android release deploy
