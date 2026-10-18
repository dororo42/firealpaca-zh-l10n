#!/usr/bin/env python3
"""生成 FireAlpaca 完整翻译清单(CSV) + 术语表(TBX)。v3: 周期切分。

实证布局: 字符串组内按 ja→zh-CN→zh-TW→ko 循环出现, 一个簇(2KB 间隔内)可能含多个周期。
周期切分: 每个"ja 段"(含假名或承接中性串的运行段)开启一个周期, 周期内按
  first(zhCN-hint)/first(zhTW-hint)/first(ko-hint) 划分四段; 中性串(纯共通汉字)按边界归属。
对齐: 周期内各段按同一 ID 顺序平行 → ja[i]↔zh[i]↔tw[i]↔ko[i]; 段短即缺号。
"""
import csv, re

PATH = '/home/doro/firealpaca/unpacked/win64/FireAlpacaWin64_2_16_3/FireAlpaca.exe'
d = open(PATH, 'rb').read()
OUT_CSV = '/home/doro/reports/2026-10-18-firealpaca-汉化翻译工作表.csv'
OUT_TBX = '/home/doro/reports/2026-10-18-firealpaca-术语表.glossary.tbx'
LO, HI = 0x5a0000, 0x660000

KANA = re.compile('[\u3040-\u30ff]')
HANGUL = re.compile('[\uac00-\ud7af]')
SIMP = set('图图层点画边关风读设语译简万与东丝两严临为举乐义习乡书买乱亏亿从众优会伞伟传价伪体余侦侧侨俭债倾偿储儿兑兰兴养内册写军农冲决况冻净凉凌减凑凛几凤凭凯击凿划刘则刚创删别剂剑剥剧劝办务动励劲劳势勋匀区医华协单卖卢卫厅历厉压厌厕厢厦厨县参双发变叙叠号叹后吓吕吗团园困围国圣坏坛坝坞坟坠垄垒垦垫墙壮声壳壶处备复够头夹夺奋奖奥妆妇妈娱婴孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尝尴尽层屉届属屡屿岁岂岗岛岭岳峡崭嵘峰币帅师帐帘帜带席帮幂并庄庆床库应庙庞废开异弃张弥弯弹强归当录彻径御忆忧怀态怂怜总恋恒恳恶恺恼悦悬悯惊惧惨惩惫惭惮惯慑愤愿懒戏战户扎扑执扩扫扬扰抚抛抡抢护报担拟拢拣拥拦拧拨择挂挚挟挠挡挣挤挥捞损捡换据掷掸揽携摄摆摇撑撵攒敛毙窃竖竞笃笋笔笼签简箩篮类粮纠红纤约级纪纬纯纱纲纳纵纶纷纸纹纺线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绢绣绥继绩绪绫续绰绳维绵绸综绽绿缀缆缉缓缔缕编缘缚缝缠缩缪缸罚罢罪置网贞负贡财责贤败账货质贩贪贫贬购贮贯贱贴贵贷贸费贺贼贾贿赂赃资赋赌赎赏赐赠赡赢赶起趋跃跄软网络检查视图窗口帮助文件编辑绘图画笔颜色图层滤镜选择动画工具')
TRAD = set('圖層點畫邊關風讀設語譯簡萬與東絲兩嚴臨為舉樂義習鄉書買亂虧億從眾優會傘偉傳價偽體餘偵側僑儉債傾償儲兒兌蘭興養內冊寫軍農衝決況凍淨涼凌減湊凜幾鳳憑凱擊鑿劃劉則剛創刪別劑劍剝劇勸辦務動勵勁勞勢勳勻區醫華協單賣盧衛廳歷厲壓厭廁廂廈廚縣參雙發變敘疊號嘆後嚇呂嗎團園困圍國聖壞壇壩塢墳墜壟壘墾墊牆壯聲殼壺處備復夠頭夾奮獎奧妝婦媽娛嬰孫學攣寧寶實寵審憲宮寬賓寢對尋導壽將爾塵嘗尷盡層屜屆屬屢嶼歲豈崗島嶼嶺嶽峽嶢峰幣帥師帳簾幟帶幫冪並莊慶床庫應廟龐廢開異棄張彌彎彈強歸當錄徹徑御憶憂懷態慫憐總戀恆懇惡愷惱悅懸憫驚懼慘懲憊慚憚慣懾憤願懶戲戰戶紮撲執擴掃揚擾撫拋掄搶護報擔擬攏揀擁攔擰撥擇掛摯挾撓擋掙擠揮撈損撿換據擲撣攜攝擺搖撐攢斂斃竊豎競篤筍筆籠簽簡籮籃類糧糾紅纖約級紀緯純紗綱納縱綸紛紙紋紡線練組紳細織終絆紹繹經綁絨結繞繪給絡絕絞統絹繡綏繼績緒綾續綽繩維綿綢綜綻綠綴纜緝緩締縷編緣縛縫纏縮繆缸罰罷罪置網貞負貢財責賢敗賬貨質販貪貧貶購貯貫賤貼貸貿費賀賊賄賂贓資賦賭贖賞賜贈贏趕起趨躍軟網絡檢查視圖窗口幫助文件編輯繪圖畫筆顏色圖層濾鏡選擇動畫工具')

def hint(t):
    if KANA.search(t): return 'ja'
    if HANGUL.search(t): return 'ko'
    sc = any(c in SIMP for c in t); tc = any(c in TRAD for c in t)
    if sc and not tc: return 'zhCN'
    if tc and not sc: return 'zhTW'
    return None

# ---- 提取 ----
strs = []
off = LO
while off < HI:
    e = d.find(b'\x00', off)
    if e < 0 or e > HI: break
    raw = d[off:e]
    if len(raw) >= 2:
        try:
            t = raw.decode('utf-8')
            if (re.search('[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', t)
                    and len(t) >= 2
                    and not any(ord(c) < 0x20 for c in t)
                    and 'function ' not in t and '<?xml' not in t):
                strs.append((off, e, t))
        except: pass
    off = e + 1

# ---- 聚类(>2KB 间隔) ----
clusters, cur = [], [strs[0]]
for s in strs[1:]:
    if s[0] - cur[-1][1] > 2048: clusters.append(cur); cur = [s]
    else: cur.append(s)
clusters.append(cur)

# ---- 运行段 + 语言清单 ----
# 各语言在簇内各自连续(次序=ID序), 但覆盖的 ID 子集不同、计数不同。
# 因此不做位置硬对齐, 改为: 每簇以 ja 清单为主表, 用 ASCII 签名做单调对齐填充 zh/tw/ko。
import difflib

def sig(s):
    """ASCII 签名: 助记符(&X)/英文词/数字是跨语言不变的强锚。"""
    toks = re.findall(r'\((&[A-Za-z])\)|[A-Za-z][A-Za-z0-9.\-]*|\d+', s)
    return tuple(toks)

def is_junk(t):
    """过滤二进制噪声: 控制字符/垃圾模式/过短。"""
    if len(t) < 2: return True
    if any(ord(c) < 0x20 for c in t): return True
    if 'function ' in t or '<?xml' in t: return True
    if re.search(r'[\u4e00-\u9fff]{1}[@\x01\x05]', t): return True
    return False

rows, stats = [], []
for ci, cl in enumerate(clusters):
    langs = {'ja': [], 'zhCN': [], 'zhTW': [], 'ko': []}
    for off, e, t in cl:
        h = hint(t)
        if h: langs[h].append(t)
        else: langs['ja'].append(t)   # 中性串默认归 ja(日文汉字词); 对不上的在对齐阶段自然落空
    n_ja = len(langs['ja'])
    if n_ja < 3 and len(langs['ko']) < 3: continue
    # 签名单调对齐: ja 为主序列, 各语言为子序列
    ja_sig = [sig(s) for s in langs['ja']]
    aligned = {}
    for lang in ('zhCN', 'zhTW', 'ko'):
        lst = langs[lang]
        sm = difflib.SequenceMatcher(None, ja_sig, [sig(s) for s in lst], autojunk=False)
        pair = {}
        conf = {}
        for a, b, sz in sm.get_matching_blocks():
            for k in range(sz):
                pair[a + k] = b + k
                # 空签名(纯 CJK 无 ASCII 锚)的位置匹配不可靠 → low; 有锚 → high
                conf[a + k] = 'high' if ja_sig[a + k] else 'low'
        aligned[lang] = (pair, conf)
    stats.append((ci, n_ja, len(langs['zhCN']), len(langs['zhTW']), len(langs['ko']),
                  langs['ja'][0][:18] if langs['ja'] else ''))
    for i, ja in enumerate(langs['ja']):
        zh, tw, ko, c_cn, c_tw = '', '', '', '', ''
        # 只填高置信配对(有 ASCII 锚); 无锚串的位置对齐不可靠, 留空交由人工比对各语言清单
        if i in aligned['zhCN'][0] and aligned['zhCN'][1][i] == 'high':
            zh = langs['zhCN'][aligned['zhCN'][0][i]]; c_cn = 'high'
        if i in aligned['zhTW'][0] and aligned['zhTW'][1][i] == 'high':
            tw = langs['zhTW'][aligned['zhTW'][0][i]]; c_tw = 'high'
        if i in aligned['ko'][0] and aligned['ko'][1][i] == 'high':
            ko = langs['ko'][aligned['ko'][0][i]]
        rows.append({'group': ci, 'idx': i, 'ja': ja, 'ko_ref': ko,
                     'zh_CN': zh, 'zh_TW': tw,
                     'status_zh_CN': 'OK' if zh else 'TO_TRANSLATE',
                     'status_zh_TW': 'OK' if tw else 'TO_TRANSLATE',
                     'align_conf': c_cn or c_tw or 'low',
                     'need_translate': 'YES' if (not zh or not tw) else ''})

cols = ['group', 'idx', 'ja', 'ko_ref', 'zh_CN', 'zh_TW',
        'status_zh_CN', 'status_zh_TW', 'align_conf', 'need_translate']
with open(OUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

# 各语言完整清单(ground truth, 二进制顺序): 对照表的行级对齐是 best-effort,
# 交接团队校对低置信行时以这四份为准。
import os
for lang, fname in (('ja', 'ja-日文源串'), ('zhCN', 'zh-CN-简中现有'),
                    ('zhTW', 'zh-TW-繁中现有'), ('ko', 'ko-韩文参考')):
    p = os.path.join(os.path.dirname(OUT_CSV), f'2026-10-18-firealpaca-l10n-{fname}.csv')
    with open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['pos', 'group', 'text'])
        # 按 hint 归属; 中性串(纯共通汉字)不入各语言清单(避免误归属), 只在对照表中按位置体现
        for ci, cl in enumerate(clusters):
            for off, e, t in cl:
                if hint(t) == lang:
                    w.writerow([off, ci, t])
    print('lang list:', p)

n_cn = sum(1 for r in rows if r['status_zh_CN'] == 'MISSING')
n_tw = sum(1 for r in rows if r['status_zh_TW'] == 'MISSING')
n_ok = sum(1 for r in rows if r['status_zh_CN'] == 'OK')
print(f'CSV: {OUT_CSV} rows={len(rows)}')
print(f'zh-CN: OK={n_ok} MISSING={n_cn} | zh-TW MISSING={n_tw} | 完整率(简中) {n_ok}/{n_ok+n_cn}')
print('\n== 簇覆盖(ja/zhCN/zhTW/ko) ==')
for ci, a, b, c, k, head in stats:
    print(f'#{ci:<3} ja={a:<4} zhCN={b:<4} zhTW={c:<4} ko={k:<4}  {head}')

# ---- TBX: 四语齐全且短(术语级)的行 ----
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
term_rows = [r for r in rows if r['ja'] and r['zh_CN'] and r['zh_TW'] and r['ko_ref']
             and len(r['ja']) <= 16 and r['status_zh_CN'] == 'OK'][:300]
tbx = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<martif type="TBX-Basic" xml:lang="ja">',
       '  <martifHeader><fileDesc><titleStmt><title>FireAlpaca UI terminology</title></titleStmt>',
       '  <sourceDesc><p>Extracted from FireAlpaca 2.16.3 binary language blocks by cn_build_worktable.py</p></sourceDesc>',
       '  </fileDesc></martifHeader>', '  <text><body>']
for i, r in enumerate(term_rows):
    tbx.append(f'    <termEntry id="e{i}">')
    for lg, key in (('ja', 'ja'), ('ko', 'ko_ref'), ('zh-CN', 'zh_CN'), ('zh-TW', 'zh_TW')):
        tbx.append(f'      <langSet xml:lang="{lg}"><tig><term>{esc(r[key])}</term></tig></langSet>')
    tbx.append('    </termEntry>')
tbx += ['  </body></text>', '</martif>']
open(OUT_TBX, 'w', encoding='utf-8').write('\n'.join(tbx))
print(f'\nTBX: {OUT_TBX} terms={len(term_rows)}')
