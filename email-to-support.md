# 邮件草稿：投递 FireAlpaca 简中/繁中翻译补全包

- 收件人：support@firealpaca.com
- 抄送：（无）
- 附件：`po/zh_CN.po`、`po/zh_TW.po`、`firealpaca-glossary.tbx`、`firealpaca-l10n-worktable-final.csv`
- 可选附件：`汉化可行性评估（中文/日本語）`——含取证细节，按需附上
- 语言：英文正文 + 日文全文（MediBang 为日本公司）
- 公开仓库（数据同源、可在线浏览/下载）：**https://github.com/dororo42/firealpaca-zh-l10n**

---

**Subject:** [Contribution] Simplified / Traditional Chinese UI translations for FireAlpaca 2.16.3 (2,672 strings + glossary)

**件名:** 【ご提供】FireAlpaca 2.16.3 の簡体字・繁体字中国語 UI 翻訳データ（2,672 文字列）

---

Dear FireAlpaca / MediBang development team,

I am an **individual FireAlpaca user and hobbyist** (not affiliated with any company or
translation team), and I use FireAlpaca daily for digital painting. While using the built-in
Chinese language option (**Help → Language → Chinese (Simplified / Traditional)**), I noticed
that both Simplified and Traditional Chinese are **only partially translated** — many UI strings
fall back to English at runtime. I would like to offer you a **complete translation dataset** for
your review and, if acceptable, for absorption into your source string tables.

All data is available in a public repository (same content as the attachments):
**https://github.com/dororo42/firealpaca-zh-l10n**

## What I found (analyzing FireAlpaca.exe 2.16.3)

- Your binary stores per-language string blocks in the order **ja → zh-CN → zh-TW → ko** within
  each string group. Group-level comparison shows both Chinese variants are missing roughly
  **30–50% of entries** (e.g. the "Color" menu group has 15 Japanese strings but only 1 Chinese
  string; the Brush-related groups miss roughly half).
- I also observed what looks like a **build-pipeline defect**: **6 Simplified Chinese strings
  (图层/粘贴/文件夹/边框/滤镜/模板) are appended at the end of the Japanese block** instead of the
  zh-CN block — likely a historical incremental patch placed in the wrong table.

## What I am offering (all data, no binaries)

1. **zh_CN.po / zh_TW.po** — gettext catalogs with **2,672 entries each** (msgid = Japanese UI
   string, msgstr = Simplified / Traditional Chinese). Placeholder integrity is verified:
   `Ctrl/Shift/Alt` key combos, `(&X)` mnemonics and numbers are preserved verbatim.
2. **firealpaca-glossary.tbx** — a TBX-Basic four-language glossary (ja / ko / zh-CN / zh-TW,
   2,672 concepts) for your terminology database.
3. **A four-language worktable (CSV)** — the full UI string inventory extracted from the binary,
   aligned as best as possible, with group/position traceability back to the binary blocks.
4. *(optional)* **A short technical report** describing the language-block layout, per-group
   coverage statistics, and the misplaced-strings evidence above.

Terminology was aligned with the community-accepted Chinese translations used by **Krita and
Blender** (e.g. レイヤー→图层/圖層, マスク→蒙版/遮色片). For the zh-TW set I followed Taiwan
conventions (滑鼠/資料夾/影像/預設) referencing Blender's `zh_TW.po` and Krita's zh_TW terminology.

## How to use

If your build keeps translations in source string tables, the CSV/PO data can be mapped by
matching the **Japanese source strings**; the `group/idx` keys in the CSV trace each entry back to
the exact position in the 2.16.3 binary, which may help your verification. If a different format
(XLIFF, plain lists, a specific CSV column order) is easier for your pipeline, I am happy to
convert. I would also appreciate any terminology corrections from your official translators, and am
glad to iterate and resubmit. If a different contact channel (e.g. your localization vendor) is
more appropriate, please let me know.

Thank you for making FireAlpaca such a great tool.

Best regards,
（署名：个人爱好者 / 日常使用者）
联系邮箱：……

---

日本語（全文）：

FireAlpaca 開発チーム／MediBang 様

私は**個人の愛好家として日々 FireAlpaca を御利用**している者です（会社・翻訳チームには
所属しておりません）。内蔵の中国語表示（**ヘルプ → 言語 → 中国語（簡体字）／（繁体字）**）
を使っていて、**簡体字・繁体字ともに翻訳が中途半端**であり、未翻訳の UI 文字列は実行時に
英語へ戻ってしまうことに気づきました。つきましては、ソースコードの文字列テーブルへの
取り込みをご検討いただきたく、**完全な中国語翻訳データ**を無償でご提供いたします。

すべてのデータは公開リポジトリにもあります（添付と同じ内容）：
**https://github.com/dororo42/firealpaca-zh-l10n**

## 発見した事実（FireAlpaca.exe 2.16.3 の解析）

- バイナリは各文字列グループ内で **ja → zh-CN → zh-TW → ko** の順に言語ブロックを格納しています。
  グループごとの比較では、簡体字・繁体字ともに**約 30〜50% の文字列が欠落**しています
  （例：「カラー」メニューグループは日本語 15 文字列に対し中国語は 1 文字列のみ；ブラシ関連グループも半数近く欠損）。
- また、**ビルドパイプラインの不具合**と考えられる現象も確認しました：**簡体字中国語 6 文字列
  （图层/粘贴/文件夹/边框/滤镜/模板）が、zh-CN ブロックではなく日本語ブロックの末尾に付加**されています
  （過去の増分パッチが誤ったテーブルに配置されたものと思われます）。

## ご提供するもの（いずれもデータのみ・バイナリなし）

1. **zh_CN.po / zh_TW.po** — gettext カタログ、**各 2,672 エントリ**（msgid = 日本語 UI 文字列、
   msgstr = 簡体字／繁体字中国語）。`Ctrl/Shift/Alt` キー組み合わせ・`(&X)` ニーモニック・数字は
   そのまま保持されています。
2. **firealpaca-glossary.tbx** — TBX-Basic 形式の 4 言語用語集（ja / ko / zh-CN / zh-TW、2,672 概念）。
3. **4 言語対照表（CSV）** — バイナリから抽出した全 UI 文字列一覧（可能な範囲で整列済み、
   バイナリ内ブロックへの位置・グループ情報付き）。
4. （任意）上記の言語ブロック構造・グループごとの欠損率・誤配置文字列の証拠をまとめた
   **簡単な技術レポート**（中国語・日本語あり）。

用語は **Krita および Blender** のコミュニティ訳（レイヤー/圖層、マスク/蒙版・遮色片 など）に
準拠しました。繁体字については Blender の `zh_TW.po` や Krita の zh_TW 用語を参照し、
台湾の慣習（滑鼠/資料夾/影像/預設）に合わせています。

## 取り込みについて

ビルドがソースの文字列テーブルで管理されている場合、CSV/PO は**日本語の原文文字列**で突合できます。
CSV の `group/idx` キーは 2.16.3 バイナリ内の正確な位置を指しており、検証にお役立ていただけます。
XLIFF やプレーンなリスト、特定の CSV 列順など、御社のパイプラインに合わせた形式への変換も可能です。
公式翻訳者による用語の修正など、フィードバックをいただければ喜んで修正・再提出いたします。
もし別の窓口（ローカライゼーション委託先など）が適切でしたらお知らせください。

日々のお絵かきを支える素晴らしいツールを作ってくださり、ありがとうございます。

以上、よろしくお願いいたします。
（署名：個人の愛好家／日々の利用者）
連絡先：……
