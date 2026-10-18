#!/usr/bin/env python3
"""汉化交付包终结: 校对后的工作表 → 规范化 → PO(zh_CN/zh_TW) + TBX + 最终 CSV。"""
import csv, re, os

SRC = '/home/doro/reports/FireAlpaca汉化翻译工作表-zh.csv'
OUT = '/home/doro/firealpaca/l10n'
os.makedirs(OUT, exist_ok=True)
os.makedirs(f'{OUT}/po', exist_ok=True)

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))

# 规范化: 日文中点 ・(U+30FB) → 中文间隔号 ·(U+00B7)
n_norm = 0
for r in rows:
    for k in ('zh_CN', 'zh_TW'):
        if '・' in r[k]:
            r[k] = r[k].replace('・', '·'); n_norm += 1
print(f'间隔号规范化: {n_norm} 行')

# ---- 最终 CSV ----
cols = ['group', 'idx', 'ja', 'ko_ref', 'zh_CN', 'zh_TW',
        'status_zh_CN', 'status_zh_TW', 'need_translate']
with open(f'{OUT}/firealpaca-l10n-worktable-final.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in cols})

# ---- PO ----
def po_esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

HEADER = (# Project-Id-Version: FireAlpaca 2.16.3
          'Project-Id-Version: FireAlpaca 2.16.3\n'
          'Language: {lang}\n'
          'MIME-Version: 1.0\n'
          'Content-Type: text/plain; charset=UTF-8\n'
          'Content-Transfer-Encoding: 8bit\n'
          'X-Source-Language: ja\n'
          'X-Note: msgid is the Japanese UI string extracted from FireAlpaca.exe language blocks; '
          'group/idx trace to the binary offsets (see l10n README).\n')

def write_po(path, lang, key):
    n = 0
    with open(path, 'w', encoding='utf-8') as f:
        f.write('msgid ""\nmsgstr ""\n')
        for line in HEADER.format(lang=lang).strip().split('\n'):
            f.write(f'"{po_esc(line)}\\n"\n')
        f.write('\n')
        for r in rows:
            if not r['ja'] or not r[key]: continue
            f.write(f'#. L10N group={r["group"]} idx={r["idx"]}\n')
            f.write(f'msgid "{po_esc(r["ja"])}"\n')
            f.write(f'msgstr "{po_esc(r[key])}"\n\n')
            n += 1
    print(f'{path}: {n} entries')

write_po(f'{OUT}/po/zh_CN.po', 'zh-CN', 'zh_CN')
write_po(f'{OUT}/po/zh_TW.po', 'zh-TW', 'zh_TW')

# ---- TBX(全量: 四语齐全的行) ----
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
tbx = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<martif type="TBX-Basic" xml:lang="ja">',
       '  <martifHeader><fileDesc><titleStmt><title>FireAlpaca UI terminology (full extraction)</title></titleStmt>',
       '  <sourceDesc><p>FireAlpaca 2.16.3 binary language blocks, aligned worktable; cn_finalize_l10n.py</p></sourceDesc>',
       '  </fileDesc></martifHeader>', '  <text><body>']
n = 0
for r in rows:
    if not (r['ja'] and r['zh_CN'] and r['zh_TW']): continue
    tbx.append(f'    <termEntry id="e{n}">')
    for lg, v in (('ja', r['ja']), ('ko', r['ko_ref']), ('zh-CN', r['zh_CN']), ('zh-TW', r['zh_TW'])):
        if v: tbx.append(f'      <langSet xml:lang="{lg}"><tig><term>{esc(v)}</term></tig></langSet>')
    tbx.append('    </termEntry>')
    n += 1
tbx += ['  </body></text>', '</martif>']
open(f'{OUT}/firealpaca-glossary.tbx', 'w', encoding='utf-8').write('\n'.join(tbx))
print(f'{OUT}/firealpaca-glossary.tbx: {n} entries')
