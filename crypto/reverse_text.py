# 字符顺序反转加密，支持中英文
# 加密：整体反转，解密：再反转一次

def encrypt(text):
    return text[::-1]

def decrypt(text):
    return text[::-1] 