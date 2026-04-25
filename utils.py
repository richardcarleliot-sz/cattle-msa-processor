import numpy as np

# ================= 极速查表优化 (ASCII -> ID) =================
CHAR_TO_ID = np.full(256, 4, dtype=np.int8)
CHAR_TO_ID[list(b'Aa')] = 0
CHAR_TO_ID[list(b'Cc')] = 1
CHAR_TO_ID[list(b'Gg')] = 2
CHAR_TO_ID[list(b'Tt')] = 3

def encode_to_ids(seq_str):
    """将字符串直接映射为底层的 0,1,2,3,4 数字数组，速度极快"""
    byte_array = np.frombuffer(seq_str.encode('ascii'), dtype=np.uint8)
    return CHAR_TO_ID[byte_array]