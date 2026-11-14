# gridline-style

Gridline 的設計系統：灰白底色、以細線構成的導軌（rails）與菱形節點、單一電光藍強調色、襯線標題字與等寬字中繼資料，支援淺色與深色模式。這裡把 [hugo-gridline](https://github.com/rubinette/hugo-gridline) 佈景主題的視覺語言整理成可重複使用的規範、樣式與模板，並以 Claude 技能（skill）的形式提供，之後將取代 zed-style。

版面語彙參考了 zed.dev 的整體結構（導軌、菱形節點、襯線標題、等寬標籤），但設計與程式碼皆為原創，不含任何 Zed 的商標、截圖或文案，也與 Zed Industries 無關。範例使用虛構產品 Orbitline。

## 內容

| 模板 | 用途 |
| --- | --- |
| `landing` | 產品首頁：主視覺、價值條、產品示意視窗、功能列、數據帶、流程展示、方案、常見問題、最新文章、行動呼籲 |
| `docs` | 文件頁：左側目錄、文章、本頁內容 |
| `changelog` | 更新紀錄：版本導軌、版本卡片、釘選欄 |
| `blog-index` | 部落格首頁：精選卡片、分類欄、依年份分組的文章列 |
| `post` | 文章頁：外側導軌標題帶、文章、目錄側欄、Mermaid 圖表 |
| `document` | A4 技術簡報，以 WeasyPrint 輸出 PDF |

每個模板都有英文與繁體中文版本（`assets/templates/<名稱>-en.html`、`-zh-tw.html`），皆為自足的單一 HTML 檔，另附填好內容的範例（`assets/examples/`）。應用程式介面沒有模板，改以 `references/app-ui.md` 說明。

## 當作技能使用

```bash
ln -s ~/src/gridline-style ~/.claude/skills/gridline-style
```

代理會從 `SKILL.md` 開始：先鎖定頁面類型、語言與輸出格式，複製對應模板填入內容，再用下列工具驗證。

```bash
python3 scripts/check.py page.html                     # 佔位符、[DATA NEEDED]、連結、錨點、樣式警告
npm install --prefix scripts                            # 第一次使用 layout.mjs 前
node scripts/layout.mjs page.html --shots shots/       # 各寬度 × 淺色／深色：水平捲動、控制項高度、主控台錯誤
uv run --no-project --with weasyprint --with pymupdf python scripts/render.py brief.html brief.pdf --png pages/
```

## 目錄結構

```
SKILL.md            代理的入口：流程與路由
CHEATSHEET.md       一頁速查：不變規則、token、類別、指令
references/         design.md（完整規範）、components.md（元件標記）、tokens.json、
                    content.md（內容規則）、mermaid.md、app-ui.md、anti-patterns.md
src/                原始碼（修改這裡）
  css/              tokens、base、construction、components、prose、blog、docs、
                    changelog、landing、diagram、syntax、print
  js/               boot.js（主題還原）、site.js（主題切換、選單、複製、目錄）、diagram.js（Pele、放大檢視）
  i18n/             介面字串（en、zh-tw）
  parts/            共用片段（頁首、頁尾、行動呼籲、圖表腳本）
  templates/        各頁面的模板原始檔
  content/          範例內容（_shared 為共用的品牌、導覽與頁尾）
assets/             由 scripts/build.py 產生（請勿手動修改）
  templates/ examples/ css/gridline.css css/print.css js/
scripts/            build.py、check.py、layout.mjs、render.py、tests/
```

## 開發流程

1. 修改 `src/` 底下的檔案。
2. 執行 `python3 scripts/build.py` 重新產生 `assets/`。
3. 執行 `python3 -m unittest discover -s scripts/tests`（其中一項測試會確認 `assets/` 與原始碼一致）與 `node scripts/layout.mjs assets/examples/*.html`。
4. 規則或數值有變動時，同步更新 `references/design.md`、`references/tokens.json`。
5. hugo-gridline 直接使用這裡的 CSS 與 JS 模組：在主題執行 `python3 scripts/sync-gridline-style.py` 同步，並檢查它的範例網站。

模板原始檔開頭的 `<!-- gridline css="…" -->` 指定要內嵌的 CSS 模組；`<!--@part:名稱-->` 引入共用片段，`[[ui:鍵]]` 會換成介面字串，`{{佔位符}}` 則保留給使用者填寫。範例內容的值若寫成 `"@檔名.html"`，會從 `src/content/` 讀入長篇 HTML。

## 授權

MIT。頁面中的 Mermaid 圖表由 [Pele](https://github.com/obsidianmd/pele)（MIT，© kepano）在瀏覽器中渲染，預設從 jsDelivr 載入；自行部署時請保留其授權檔。字型只列出字型名稱（IBM Plex、Lilex 等開源字型優先），不嵌入或連結字型檔。
