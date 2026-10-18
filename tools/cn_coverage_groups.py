#!/usr/bin/env python3
"""分组级覆盖分析: 以 ko(最全)块为锚, 检查每组的 ja/zh-CN/zh-TW 块是否存在。
布局假设(已实证): 每个字符串组内按 ja→zh-CN→zh-TW→ko 顺序连续存放 4 个语言子块。"""
import re, collections

PATH = '/home/doro/firealpaca/unpacked/win64/FireAlpacaWin64_2_16_3/FireAlpaca.exe'
d = open(PATH, 'rb').read()
LO, HI = 0x5a0000, 0x660000   # 主 UI 串区

KANA = re.compile('[\u3040-\u30ff]')
HANGUL = re.compile('[\uac00-\ud7af]')
SIMP = set('图层点画边关风读设语译简万与东丝两严临为举乐义习乡书买乱亏亿从众优会伞伟传价伪体余侦侧侨俭债倾偿储儿兑兰兴养内册写军农冲决况冻净凉凌减凑凛几凤凭凯击凿划刘则刚创删别剂剑剥剧劝办务动励劲劳势勋匀区医华协单卖卢卫厅历厉压厌厕厢厦厨县参双发变叙叠号叹后吓吕吗团园困围国圣坏坛坝坞坟坠垄垒垦垫墙壮声壳壶处备复够头夹夺奋奖奥妆妇妈娱婴孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尝尴尽层屉届属屡屿岁岂岗岛岭岳峡崭嵘峰币帅师帐帘帜带席帮幂并庄庆床库应庙庞废开异弃张弥弯弹强归当录彻径御忆忧怀态怂怜总恋恒恳恶恺恼悦悬悯惊惧惨惩惫惭惮惯慑愤愿懒戏战户扎扑执扩扫扬扰抚抛抡抢护报担拟拢拣拥拦拧拨择挂挚挟挠挡挣挤挥捞损捡换据掷掸揽携摄摆摇撑撵攒敛毙窃竖竞笃笋笔笼签简箩篮类粮纠红纤约级纪纬纯纱纲纳纵纶纷纸纹纺线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绢绣绥继绩绪绫续绰绳维绵绸综绽绿缀缆缉缓缔缕编缘缚缝缠缩缪缸罚罢罪置网贞负贡财责贤败账货质贩贪贫贬购贮贯贱贴贵贷贸费贺贼贾贿赂赃资赋赌赎赏赐赠赡赢赶起趋跃跄软网络检查视图窗口帮助文件编辑绘图画笔颜色图层滤镜选择动画工具')
TRAD = set('圖層點畫邊關風讀設語譯簡萬與東絲兩嚴臨為舉樂義習鄉書買亂虧億從眾優會傘偉傳價偽體餘偵側僑儉債傾償儲兒兌蘭興養內冊寫軍農衝決況凍淨涼凌減湊凜幾鳳憑凱擊鑿劃劉則剛創刪別劑劍剝劇勸辦務動勵勁勞勢勳勻區醫華協單賣盧衛廳歷厲壓厭廁廂廈廚縣參雙發變敘疊號嘆後嚇呂嗎團園困圍國聖壞壇壩塢墳墜壟壘墾墊牆壯聲殼壺處備復夠頭夾奮獎奧妝婦媽娛嬰孫學攣寧寶實寵審憲宮寬賓寢對尋導壽將爾塵嘗尷盡層屜屆屬屢嶼歲豈崗島嶼嶺嶽峽嶢峰幣帥師帳簾幟帶幫冪並莊慶床庫應廟龐廢開異棄張彌彎彈強歸當錄徹徑御憶憂懷態慫憐總戀恆懇惡愷惱悅懸憫驚懼慘懲憊慚憚慣懾憤願懶戲戰戶紮撲執擴掃揚擾撫拋掄搶護報擔擬攏揀擁攔擰撥擇掛摯挾撓擋掙擠揮撈損撿換據擲撣攜攝擺搖撐攢斂斃竊豎競篤筍筆籠簽簡籮籃類糧糾紅纖約級紀緯純紗綱納縱綸紛紙紋紡線練組紳細織終絆紹繹經綁絨結繞繪給絡絕絞統絹繡綏繼績緒綾續綽繩維綿綢綜綻綠綴纜緝緩締縷編緣縛縫纏縮繆缸罰罷罪置網貞負貢財責賢敗賬貨質販貪貧貶購貯貫賤貼貸貿費賀賊賄賂贓資賦賭贖賞賜贈贏趕起趨躍軟網絡檢查視圖窗口幫助文件編輯繪圖畫筆顏色圖層濾鏡選擇動畫工具')

def lang_of(t):
    if KANA.search(t): return 'ja'
    if HANGUL.search(t): return 'ko'
    sc = sum(1 for ch in t if ch in SIMP); tc = sum(1 for ch in t if ch in TRAD)
    if sc and not tc: return 'zh-CN'
    if tc and not sc: return 'zh-TW'
    if re.search('[\u4e00-\u9fff]', t): return 'han'
    return None

# 提取全部 CJK 串
strs = []   # (off, end, lang, text)
off = LO
while off < HI:
    e = d.find(b'\x00', off)
    if e < 0 or e > HI: break
    raw = d[off:e]
    if len(raw) >= 4:
        try:
            t = raw.decode('utf-8')
            L = lang_of(t)
            if L: strs.append((off, e, L, t))
        except: pass
    off = e + 1

# 聚类: 间隔 > 2KB 视为新组
groups = []
cur = [strs[0]]
for s in strs[1:]:
    if s[0] - cur[-1][1] > 2048:
        groups.append(cur); cur = [s]
    else:
        cur.append(s)
groups.append(cur)

print(f'总串数 {len(strs)}, 组数 {len(groups)}')
print(f"{'组#':>4} {'ja':>4} {'zhCN':>4} {'zhTW':>4} {'ko':>4} {'han':>4}  首串")
gaps = {'ja': 0, 'zh-CN': 0, 'zh-TW': 0}
for gi, g in enumerate(groups):
    c = collections.Counter(x[2] for x in g)
    mark = ' <== 缺' if (c['ko'] >= 3 and (c['zh-CN'] == 0 or c['zh-TW'] == 0)) else ''
    if c['ko'] >= 3 and (c['zh-CN'] == 0 or c['zh-TW'] == 0):
        gaps['ja'] += (1 if c['ja'] else 0)
        gaps['zh-CN'] += (0 if c['zh-CN'] else 1)
        gaps['zh-TW'] += (0 if c['zh-TW'] else 1)
    if gi < 40 or mark:
        print(f'{gi:>4} {c["ja"]:>4} {c["zh-CN"]:>4} {c["zh-TW"]:>4} {c["ko"]:>4} {c["han"]:>4}  {g[0][3][:24]!r}{mark}')
print('\n== 有 ko>=3 条但缺简中/繁中子块的组数 ==')
print(gaps)
