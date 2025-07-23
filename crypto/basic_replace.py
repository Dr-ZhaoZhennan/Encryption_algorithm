# 基础替换加密，支持中英文
# 加密表：a→x, b→y, ..., 你→好, 好→你, ...
replace_map = {
    'a': 'x', 'b': 'y', 'c': 'z', 'd': 'w', 'e': 'v', 'f': 'u', 'g': 't', 'h': 's', 'i': 'r', 'j': 'q',
    'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l', 'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g',
    'u': 'f', 'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b', 'z': 'a',
    'A': 'X', 'B': 'Y', 'C': 'Z', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S', 'I': 'R', 'J': 'Q',
    'K': 'P', 'L': 'O', 'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I', 'S': 'H', 'T': 'G',
    'U': 'F', 'V': 'E', 'W': 'D', 'X': 'C', 'Y': 'B', 'Z': 'A',
    '你': '好', '好': '你', '中': '华', '华': '中', '国': '人', '人': '国'
}
reverse_map = {v: k for k, v in replace_map.items()}

def encrypt(text):
    return ''.join(replace_map.get(c, c) for c in text)

def decrypt(text):
    return ''.join(reverse_map.get(c, c) for c in text) 