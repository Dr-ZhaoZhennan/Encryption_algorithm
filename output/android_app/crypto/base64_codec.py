# Base64加密，支持中英文
# 加密：文本转为UTF-8字节后Base64编码，解密：Base64解码还原
import base64

def encrypt(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8') 