# 设置窗口类
# 用于管理密钥和其他加密参数

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QGroupBox, QMessageBox, QSpinBox,
    QTextEdit, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import os
from crypto.key_transform import generate_random_key, validate_key

class SettingsWindow(QWidget):
    # 信号：设置已保存
    settings_saved = pyqtSignal(dict)
    
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.current_settings = current_settings or {}
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle('加密设置')
        self.setFixedSize(500, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'ico.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel('加密算法设置')
        title_label.setFont(QFont('微软雅黑', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('color: #333; margin-bottom: 10px;')
        main_layout.addWidget(title_label)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 密钥设置组
        key_group = self.create_key_group()
        main_layout.addWidget(key_group)
        
        # 加密选项组
        options_group = self.create_options_group()
        main_layout.addWidget(options_group)
        
        # 按钮组
        button_layout = self.create_button_layout()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: '微软雅黑';
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #333;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#secondary {
                background-color: #2196F3;
            }
            QPushButton#secondary:hover {
                background-color: #1976D2;
            }
            QPushButton#cancel {
                background-color: #f44336;
            }
            QPushButton#cancel:hover {
                background-color: #d32f2f;
            }
            QCheckBox {
                font-size: 12px;
                color: #333;
            }
            QLabel {
                color: #333;
                font-size: 12px;
            }
        """)
    
    def create_key_group(self):
        """创建密钥设置组"""
        group = QGroupBox('密钥设置')
        layout = QVBoxLayout()
        
        # 启用密钥选项
        self.enable_key_checkbox = QCheckBox('启用密钥加密（增强安全性）')
        self.enable_key_checkbox.stateChanged.connect(self.on_key_enabled_changed)
        layout.addWidget(self.enable_key_checkbox)
        
        # 密钥输入区域
        self.key_widget = QWidget()
        key_layout = QVBoxLayout()
        
        # 密钥输入
        key_input_layout = QHBoxLayout()
        key_input_layout.addWidget(QLabel('密钥:'))
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('请输入8-32位密钥（数字+字母组合）')
        self.key_input.textChanged.connect(self.validate_key_input)
        key_input_layout.addWidget(self.key_input)
        
        # 随机生成按钮
        self.generate_key_btn = QPushButton('随机生成密钥')
        self.generate_key_btn.setObjectName('secondary')
        self.generate_key_btn.clicked.connect(self.generate_random_key)
        key_input_layout.addWidget(self.generate_key_btn)
        
        key_layout.addLayout(key_input_layout)
        
        # 密钥长度设置
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel('生成密钥长度:'))
        
        self.key_length_spin = QSpinBox()
        self.key_length_spin.setRange(8, 32)
        self.key_length_spin.setValue(16)
        length_layout.addWidget(self.key_length_spin)
        length_layout.addWidget(QLabel('位'))
        length_layout.addStretch()
        
        key_layout.addLayout(length_layout)
        
        # 密钥验证提示
        self.key_status_label = QLabel('')
        self.key_status_label.setWordWrap(True)
        key_layout.addWidget(self.key_status_label)
        
        # 密钥说明
        key_info = QTextEdit()
        key_info.setMaximumHeight(80)
        key_info.setReadOnly(True)
        key_info.setText(
            "密钥说明：\n"
            "• 密钥用于对加密结果进行二次变换，大大增强安全性\n"
            "• 必须包含数字和字母的组合，长度8-32位\n"
            "• 解密时需要使用相同的密钥"
        )
        key_info.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 11px;
                color: #666;
            }
        """)
        key_layout.addWidget(key_info)
        
        self.key_widget.setLayout(key_layout)
        layout.addWidget(self.key_widget)
        
        group.setLayout(layout)
        return group
    
    def create_options_group(self):
        """创建其他选项组"""
        group = QGroupBox('其他选项')
        layout = QVBoxLayout()
        
        # 自动复制结果
        self.auto_copy_checkbox = QCheckBox('加密/解密后自动复制结果到剪贴板')
        layout.addWidget(self.auto_copy_checkbox)
        
        # 保存密钥
        self.save_key_checkbox = QCheckBox('记住密钥设置（下次启动时自动加载）')
        layout.addWidget(self.save_key_checkbox)
        
        group.setLayout(layout)
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 取消按钮
        cancel_btn = QPushButton('取消')
        cancel_btn.setObjectName('cancel')
        cancel_btn.clicked.connect(self.close)
        layout.addWidget(cancel_btn)
        
        # 保存按钮
        save_btn = QPushButton('保存设置')
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        return layout
    
    def on_key_enabled_changed(self, state):
        """密钥启用状态改变"""
        enabled = state == Qt.Checked
        self.key_widget.setEnabled(enabled)
        
        if enabled:
            self.validate_key_input()
        else:
            self.key_status_label.setText('')
    
    def validate_key_input(self):
        """验证密钥输入"""
        key = self.key_input.text()
        
        if not key:
            self.key_status_label.setText('')
            return
        
        is_valid, error_msg = validate_key(key)
        
        if is_valid:
            self.key_status_label.setText('✓ 密钥格式正确')
            self.key_status_label.setStyleSheet('color: green; font-weight: bold;')
        else:
            self.key_status_label.setText(f'✗ {error_msg}')
            self.key_status_label.setStyleSheet('color: red; font-weight: bold;')
    
    def generate_random_key(self):
        """生成随机密钥"""
        length = self.key_length_spin.value()
        key = generate_random_key(length)
        self.key_input.setText(key)
        
        # 显示生成成功消息
        QMessageBox.information(self, '密钥生成', f'已生成{length}位随机密钥！\n\n请妥善保管此密钥，解密时需要使用。')
    
    def load_settings(self):
        """加载当前设置"""
        # 加载密钥设置
        key_enabled = self.current_settings.get('key_enabled', False)
        self.enable_key_checkbox.setChecked(key_enabled)
        
        key = self.current_settings.get('key', '')
        self.key_input.setText(key)
        
        # 加载其他选项
        auto_copy = self.current_settings.get('auto_copy', False)
        self.auto_copy_checkbox.setChecked(auto_copy)
        
        save_key = self.current_settings.get('save_key', True)
        self.save_key_checkbox.setChecked(save_key)
        
        # 触发验证
        self.on_key_enabled_changed(Qt.Checked if key_enabled else Qt.Unchecked)
    
    def save_settings(self):
        """保存设置"""
        # 验证密钥
        key_enabled = self.enable_key_checkbox.isChecked()
        key = self.key_input.text()
        
        if key_enabled and key:
            is_valid, error_msg = validate_key(key)
            if not is_valid:
                QMessageBox.warning(self, '密钥错误', f'密钥格式不正确：\n{error_msg}')
                return
        
        # 收集设置
        settings = {
            'key_enabled': key_enabled,
            'key': key if key_enabled else '',
            'auto_copy': self.auto_copy_checkbox.isChecked(),
            'save_key': self.save_key_checkbox.isChecked()
        }
        
        # 发送信号
        self.settings_saved.emit(settings)
        
        # 显示保存成功消息
        QMessageBox.information(self, '设置保存', '设置已保存成功！')
        
        # 关闭窗口
        self.close()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        super().closeEvent(event)