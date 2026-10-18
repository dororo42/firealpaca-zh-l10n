#!/usr/bin/env python3
"""核实内置简中覆盖度 v2: NUL 分割全串扫描 + 语言分类 + 区域映射。"""
import re, collections

PATH = '/home/doro/firealpaca/unpacked/win64/FireAlpacaWin64_2_16_3/FireAlpaca.exe'
d = open(PATH, 'rb').read()

KANA = re.compile('[\u3040-\u30ff]')
HANGUL = re.compile('[\uac00-\ud7af]')
SIMP = set('图图层点画边关风读设语译简万与东丝两严临为举乐义习乡书买乱亏亿从众优会伞伟传价伪体余侦侧侨俭债倾偿储儿兑兰兴养内册写军农冲决况冻净凉凌减凑凛几凤凭凯击凿划刘则刚创删别剂剑剥剧劝办务动励劲劳势勋匀区医华协单卖卢卫厅历厉压厌厕厢厦厨县参双发变叙叠号叹后吓吕吗团园困围国圣坏坛坝坞坟坠垄垒垦垫墙壮声壳壶处备复够头夹夺奋奖奥妆妇妈娱婴孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尝尴尽层屉届属屡屿岁岂岗岛岭岳峡崭嵘峰币帅师帐帘帜带席帮幂并庄庆床库应庙庞废开异弃张弥弯弹强归当录彻径御忆忧怀态怂怜总恋恒恳恶恺恼悦悬悯惊惧惨惩惫惭惮惯慑愤愿懒戏战户扎扑执扩扫扬扰抚抛抡抢护报担拟拢拣拥拦拧拨择挂挚挟挠挡挣挤挥捞损捡换据掷掸揽携摄摆摇撑撵攒敛毙窃竖竞笃笋笔笼签简箩篮类粮纠红纤约级纪纬纯纱纲纳纵纶纷纸纹纺线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绢绣绥继绩绪绫续绰绳维绵绸综绽绿缀缆缉缓缔缕编缘缚缝缠缩缪缸罚罢罪置网贞负贡财责贤败账货质贩贪贫贬购贮贯贱贴贵贷贸费贺贼贾贿赂赃资赋赌赎赏赐赠赡赢赶起趋跃跄软网络检查视图窗口帮助文件编辑绘图画笔颜色图层滤镜选择动画工具')
TRAD = set('圖層點畫邊關風讀設語譯簡萬與東絲兩嚴臨為舉樂義習鄉書買亂虧億從眾優會傘偉傳價偽體餘偵側僑儉債傾償儲兒兌蘭興養內冊寫軍農衝決況凍淨涼凌減湊凜幾鳳憑凱擊鑿劃劉則剛創刪別劑劍剝劇勸辦務動勵勁勞勢勳勻區醫華協單賣盧衛廳歷厲壓厭廁廂廈廚縣參雙發變敘疊號嘆後嚇呂嗎團園困圍國聖壞壇壩塢墳墜壟壘墾墊牆壯聲殼壺處備復夠頭夾奮獎奧妝婦媽娛嬰孫學攣寧寶實寵審憲宮寬賓寢對尋導壽將爾塵嘗尷盡層屜屆屬屢嶼歲豈崗島嶺嶽峽嶢峰嶗幣帥師帳簾幟帶席幫冪並莊慶床庫應廟龐廢開異棄張彌彎彈強歸當錄徹徑御憶憂懷態慫憐總戀恆懇惡愷惱悅懸憫驚懼慘懲憊慚憚慣懾憤願懶戲戰戶紮撲執擴掃揚擾撫拋掄搶護報擔擬攏揀擁攔擰撥擇掛摯挾撓擋掙擠揮撈損撿換據擲撣攜攝擺搖撐攢斂斃竊豎競篤筍筆籠簽簡籮籃類糧糾紅纖約級紀緯純紗綱納縱綸紛紙紋紡線練組紳細織終絆紹繹經綁絨結繞繪給絡絕絞統絹繡綏繼績緒綾續綽繩維綿綢綜綻綠綴纜緝緩締縷編緣縛縫纏縮繆缸罰罷罪置網貞負貢財責賢敗賬貨質販貪貧貶購貯貫賤貼貸貿費賀賊賄賂贓資賦賭贖賞賜贈贏趕起趨躍軟網絡檢查視圖窗口幫助文件編輯繪圖畫筆顏色圖層濾鏡選擇動畫工具')

def classify(t):
    if KANA.search(t): return 'ja'
    if HANGUL.search(t): return 'ko'
    sc = sum(1 for ch in t if ch in SIMP)
    tc = sum(1 for ch in t if ch in TRAD)
    if sc and not tc: return 'zh-CN'
    if tc and not sc: return 'zh-TW'
    if sc and tc: return 'han-mixed'
    if re.search('[\u4e00-\u9fff]', t): return 'han-neutral'
    return None

cnt = collections.Counter()
runs = []   # (lang, start_off, end_off, count) 连续同语言游程
cur = None
off = 0x400000
step_samples = collections.defaultdict(list)
while off < 0x700000:
    e = d.find(b'\x00', off)
    if e < 0: break
    raw = d[off:e]
    if len(raw) >= 4:
        try: t = raw.decode('utf-8')
        except:
            off = e + 1; continue
        if re.search('[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', t):
            c = classify(t)
            cnt[c] += 1
            if len(step_samples[c]) < 5: step_samples[c].append((hex(off), t[:32]))
            runs.append((off, e, c, t))
    off = e + 1

print('== 语言分类计数 (扫描 0x400000-0x700000) ==')
for k, v in cnt.most_common():
    print(f'{k:12s} {v}')
for k in step_samples:
    print(f'-- {k}:')
    for a, t in step_samples[k]: print(f'   {a}  {t}')

# 连续游程: 按语言聚合出块边界
print('\n== 主要语言块(同语言连续 >=8 条) ==')
blocks = []
i = 0
while i < len(runs):
    j = i
    while j < len(runs) and runs[j][2] == runs[i][2] and runs[j][0] - (runs[j-1][1] if j > i else runs[j][0]) < 4096:
        j += 1
    if j - i >= 8:
        blocks.append((runs[i][2], hex(runs[i][0]), hex(runs[j-1][1]), j - i))
    i = max(j, i + 1)
for b in blocks[:24]:
    print(f'{b[0]:8s} {b[1]}-{b[2]}  n={b[3]}')
