# 密钥生成和变换模块
# 支持随机生成密钥和基于密钥的字符变换

import random
import string
import time
import hashlib
import math

def gcd(a, b):
    """
    计算最大公约数
    """
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    扩展欧几里得算法
    """
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a, m):
    """
    计算模逆元素
    """
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError(f"模逆不存在: gcd({a}, {m}) = {gcd_val}")
    return (x % m + m) % m

def generate_random_key(length=16):
    """
    生成随机密钥，包含数字和字母的组合
    :param length: 密钥长度，默认16位
    :return: 随机密钥字符串
    """
    # 使用时间种子确保每次生成的密钥都不同
    random.seed(int(time.time() * 1000000) % 2147483647)
    
    # 确保密钥包含数字和字母
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    key = ''.join(random.choice(chars) for _ in range(length))
    
    # 确保至少包含一个数字和一个字母
    if not any(c.isdigit() for c in key):
        key = key[:-1] + random.choice(string.digits)
    if not any(c.isalpha() for c in key):
        key = key[:-1] + random.choice(string.ascii_letters)
    
    return key

def validate_key(key):
    """
    验证密钥格式是否正确
    :param key: 密钥字符串
    :return: (是否有效, 错误信息)
    """
    if not key:
        return False, "密钥不能为空"
    
    if len(key) < 8:
        return False, "密钥长度至少8位"
    
    if len(key) > 32:
        return False, "密钥长度不能超过32位"
    
    # 检查是否只包含字母和数字
    if not all(c.isalnum() for c in key):
        return False, "密钥只能包含字母和数字"
    
    # 检查是否至少包含一个字母和一个数字
    has_letter = any(c.isalpha() for c in key)
    has_digit = any(c.isdigit() for c in key)
    
    if not has_letter:
        return False, "密钥必须包含至少一个字母"
    
    if not has_digit:
        return False, "密钥必须包含至少一个数字"
    
    return True, ""

def key_to_transform_sequence(key):
    """
    将密钥转换为复杂变换序列
    :param key: 密钥字符串
    :return: 变换参数字典列表
    """
    # 使用MD5哈希确保密钥的一致性变换
    key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    
    # 将哈希值转换为复杂变换参数
    transforms = []
    for i in range(0, len(key_hash), 8):  # 每8个字符生成一组变换参数
        chunk = key_hash[i:i+8]
        if len(chunk) < 8:
            chunk = chunk.ljust(8, '0')  # 补齐到8位
        
        # 生成多个变换参数
        a = (int(chunk[0:2], 16) % 32767) + 2  # 乘法因子，确保与65536互质
        b = int(chunk[2:4], 16) * 256 + int(chunk[4:6], 16)  # 加法偏移，16位
        c = int(chunk[6:7], 16) % 16  # 位移量，0-15
        d = int(chunk[7:8], 16) * 16 + (int(chunk[0:1], 16) % 16)  # XOR掩码，8位
        
        # 确保a与65536互质（用于模逆运算）
        while gcd(a, 65536) != 1:
            a = (a + 1) % 65536
            if a < 2:
                a = 3  # 3与65536互质
        
        transforms.append({
            'mult': a,      # 乘法因子
            'add': b,       # 加法偏移
            'shift': c,     # 位移量
            'xor': d        # XOR掩码
        })
    
    return transforms

def apply_key_transform(text, key, encrypt=True):
    """
    使用密钥对文本进行复杂数学变换
    :param text: 要变换的文本
    :param key: 密钥
    :param encrypt: True为加密，False为解密
    :return: 变换后的文本
    """
    if not text:
        return text
    
    # 验证密钥
    is_valid, error_msg = validate_key(key)
    if not is_valid:
        raise ValueError(f"密钥无效: {error_msg}")
    
    # 获取变换序列
    transforms = key_to_transform_sequence(key)
    
    result = []
    for i, char in enumerate(text):
        # 使用循环的变换序列
        transform_index = i % len(transforms)
        params = transforms[transform_index]
        
        char_code = ord(char)
        
        if encrypt:
            # 复杂加密变换：多步骤可逆变换
            # 步骤1: 仿射变换 (ax + b) mod 65536
            step1 = (char_code * params['mult'] + params['add']) % 65536
            # 步骤2: 位运算 - 循环左移
            shift_amount = params['shift'] % 16
            step2 = ((step1 << shift_amount) | (step1 >> (16 - shift_amount))) & 0xFFFF
            # 步骤3: XOR变换
            new_code = step2 ^ (params['xor'] | (params['xor'] << 8))
        else:
            # 复杂解密变换：严格逆向操作
            # 步骤3逆: XOR逆变换
            step3_inv = char_code ^ (params['xor'] | (params['xor'] << 8))
            # 步骤2逆: 循环右移
            shift_amount = params['shift'] % 16
            step2_inv = ((step3_inv >> shift_amount) | (step3_inv << (16 - shift_amount))) & 0xFFFF
            # 步骤1逆: 仿射逆变换
            mult_inv = mod_inverse(params['mult'], 65536)
            new_code = (mult_inv * (step2_inv - params['add'])) % 65536
        
        # 确保结果在合理的Unicode范围内
        new_code = new_code % 65536
        if new_code == 0:
            new_code = 1
        
        result.append(chr(new_code))
    
    return ''.join(result)

def encrypt_with_key(text, key):
    """
    使用密钥加密文本
    :param text: 明文
    :param key: 密钥
    :return: 密文
    """
    return apply_key_transform(text, key, encrypt=True)

def decrypt_with_key(text, key):
    """
    使用密钥解密文本
    :param text: 密文
    :param key: 密钥
    :return: 明文
    """
    return apply_key_transform(text, key, encrypt=False)