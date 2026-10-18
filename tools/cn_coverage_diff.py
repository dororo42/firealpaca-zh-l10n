#!/usr/bin/env python3
"""逐条对比 ja / zh-CN / zh-TW / ko 平行块, 输出简中缺失清单。"""
import re

PATH = '/home/doro/firealpaca/unpacked/win64/FireAlpacaWin64_2_16_3/FireAlpaca.exe'
d = open(PATH, 'rb').read()

def block(off, end):
    """取 [off,end) 内按 NUL 分割的字符串列表。"""
    out = []
    o = off
    while o < end:
        e = d.find(b'\x00', o)
        if e < 0 or e > end: e = end
        s = d[o:e]
        if s: out.append((o, s))
        o = e + 1
    return out

# 已知平行块(第一组: 菜单层)
ja  = block(0x5af7d8, 0x5afec0)
cn  = block(0x5afec0, 0x5b00f0)   # zh-CN 块直到下一个非 zh 串
tw  = block(0x5b00f0, 0x5b06b0)   # 含 zh-TW 与其中性串
ko  = block(0x5b06b0, 0x5b0d10)

def txt(items): return [s.decode('utf-8', 'replace') for _, s in items]

ja_t, cn_t, tw_t, ko_t = txt(ja), txt(cn), txt(tw), txt(ko)
print(f'ja={len(ja_t)} zh-CN={len(cn_t)} zh-TW={len(tw_t)} ko={len(ko_t)}')
print('\n-- ja 块全列 --')
for i, s in enumerate(ja_t): print(f'{i:3d} {s}')
print('\n-- zh-CN 块全列 --')
for i, s in enumerate(cn_t): print(f'{i:3d} {s}')
print('\n-- zh-TW 块全列 --')
for i, s in enumerate(tw_t): print(f'{i:3d} {s}')
