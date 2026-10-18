# 邮件草稿：投递 FireAlpaca 简中/繁中翻译补全包

- 收件人：support@firealpaca.com
- 抄送：（无）
- 附件：`po/zh_CN.po`、`po/zh_TW.po`、`firealpaca-glossary.tbx`、`firealpaca-l10n-worktable-final.csv`、`汉化可行性与工作量评估.md`
- 语言：英文正文 + 日文摘要（MediBang 为日本公司，双语确保传达）

---

**Subject:** [Contribution] Complete Simplified/Traditional Chinese translations for FireAlpaca 2.16.3 (2,672 UI strings + glossary)

**件名:** 【ご提供】FireAlpaca 2.16.3 の簡体字・繁体字中国語 UI 翻訳完全版（2,672 文字列）

---

Dear FireAlpaca development team,

We are an independent research group working on FireAlpaca localization analysis. While using the
built-in Chinese language option (Help → Language), we noticed that both Simplified and Traditional
Chinese are **partially translated** — many UI strings fall back to English. We would like to offer
you a complete translation dataset for your review and, if acceptable, for absorption into your
source string tables.

## What we found (from analyzing FireAlpaca.exe 2.16.3)

- Your binary ships per-language string blocks in the order ja → zh-CN → zh-TW → ko within each
  string group. Group-level comparison shows both Chinese variants are missing roughly **30–50% of
  entries** (e.g. the "Color" menu group has 15 Japanese strings but only 1 Chinese string).
- We also observed what appears to be a build-pipeline defect: **6 Simplified Chinese strings
  (图层/粘贴/文件夹/边框/滤镜/模板) are appended at the end of the Japanese block** instead of the
  zh-CN block — likely a historical incremental patch placed in the wrong table.

## What we are offering (all data, no binaries)

1. **zh_CN.po / zh_TW.po** — gettext catalogs with **2,672 entries each** (msgid = Japanese UI
   string, msgstr = Simplified / Traditional Chinese). Placeholder integrity is verified:
   `Ctrl/Shift/Alt` key combos, `(&X)` mnemonics and numbers are preserved verbatim.
2. **firealpaca-glossary.tbx** — a TBX-Basic four-language glossary (ja / ko / zh-CN / zh-TW,
   2,672 concepts) for your terminology database.
3. **A four-language worktable (CSV)** — the full UI string inventory extracted from the binary,
   aligned as best as possible, with group/position traceability back to the binary blocks.
4. **A short technical report** describing the language-block layout, per-group coverage statistics,
   and the misplaced-strings evidence above.

Terminology was aligned with the community-accepted Chinese translations used by Krita and Blender
(e.g. レイヤー→图层/圖層, マスク→蒙版/遮色片), and style follows common Chinese software UI
conventions (including Taiwan-specific vocabulary such as 滑鼠/資料夾/影像 in the zh-TW set).

## How to use

If your build stores translations in source string tables, the CSV/PO data can be mapped by matching
the Japanese source strings; the `group/idx` keys in the CSV trace each entry back to the exact
position in the 2.16.3 binary, in case that helps your verification. If a different format (XLIFF,
CSV column order, plain lists) is easier for your pipeline, we are happy to convert.

We would appreciate any feedback — including terminology corrections from your official translators;
we are glad to iterate and resubmit. Please also let us know if a different contact channel
(e.g. your localization vendor) is more appropriate for this kind of contribution.

Thank you for making FireAlpaca such a great tool.

Best regards,
（署名/团队名）
联系邮箱：……

---

日本語要約：

FireAlpaca 2.16.3 の多言語リソースを解析したところ、簡体字・繁体字中国語の UI 翻訳に
欠損（グループごとに約 30〜50%）があることを確認しました。つきましては、不足分を含む
**2,672 文字列の完全な中国語訳**（gettext PO 形式・TBX 用語集・ four 言語対照表）を
無償でご提供いたします。ソースコードの文字列テーブルへの取り込みをご検討いただければ幸いです。
なお、日本語ブロック末尾に簡体字中国語 6 文字列が混在している現象も確認しており、
詳細資料に証跡を添付してあります。ご検討のほど、よろしくお願いいたします。
