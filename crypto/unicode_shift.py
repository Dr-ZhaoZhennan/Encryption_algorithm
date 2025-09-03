# Unicode码位移加密，支持中英文
# 加密：每个字符的Unicode码+3，解密：每个字符的Unicode码-3
# 支持密钥增强加密
from . import key_transform

OFFSET = 3

def encrypt(text, key=None):
    """Unicode位移加密
    :param text: 明文
    :param key: 可选密钥，如果提供则进行密钥增强
    :return: 密文
    """
    if not text:
        return text
    
    # 基础Unicode位移
    result = ''.join(chr(ord(c) + OFFSET) for c in text)
    
    # 如果提供了密钥，进行额外的密钥变换
    if key:
        result = key_transform.encrypt_with_key(result, key)
    
    return result

def decrypt(text, key=None):
    """Unicode位移解密
    :param text: 密文
    :param key: 可选密钥，如果提供则进行密钥解密
    :return: 明文
    """
    if not text:
        return text
    
    result = text
    
    # 如果提供了密钥，先进行密钥解密
    if key:
        result = key_transform.decrypt_with_key(result, key)
    
    # 基础Unicode位移解密
    result = ''.join(chr(ord(c) - OFFSET) for c in result)
    
    return result