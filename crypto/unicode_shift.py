# Unicode码位移加密，支持中英文
# 加密：每个字符的Unicode码+3，解密：每个字符的Unicode码-3
OFFSET = 3

def encrypt(text):
    return ''.join(chr(ord(c) + OFFSET) for c in text)

def decrypt(text):
    return ''.join(chr(ord(c) - OFFSET) for c in text) 