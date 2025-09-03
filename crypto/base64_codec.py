# Base64加密，支持中英文
# 加密：文本转为UTF-8字节后Base64编码，解密：Base64解码还原
# 支持密钥增强加密
import base64
from . import key_transform

def encrypt(text, key=None):
    """Base64加密
    :param text: 明文
    :param key: 可选密钥，如果提供则进行密钥增强
    :return: 密文
    """
    if not text:
        return text
    
    # 如果提供了密钥，先进行密钥变换
    if key:
        text = key_transform.encrypt_with_key(text, key)
    
    # Base64编码
    result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    return result

def decrypt(text, key=None):
    """Base64解密
    :param text: 密文
    :param key: 可选密钥，如果提供则进行密钥解密
    :return: 明文
    """
    if not text:
        return text
    
    # Base64解码
    result = base64.b64decode(text.encode('utf-8')).decode('utf-8')
    
    # 如果提供了密钥，进行密钥解密
    if key:
        result = key_transform.decrypt_with_key(result, key)
    
    return result