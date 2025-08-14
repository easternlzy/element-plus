### 海报模板与快速使用指南

这些模板为可编辑的 SVG（矢量）文件，适合打印（A4）与社交媒体（1080×1920）。你可以直接在浏览器或设计软件中打开与修改，或使用随附脚本批量替换占位符并输出到新目录。

- **预览模板**: 直接用浏览器或设计软件打开 `posters/*.svg`
- **一键渲染**: 使用示例数据替换占位符，输出到 `build/`
```bash
python3 /workspace/posters/render_posters.py \
  --data /workspace/posters/sample-data.json \
  --outdir /workspace/posters/build
```
- **自定义你的内容**: 复制 `sample-data.json` 修改成你的文案与信息，再运行上面的命令
- **导出 PNG / PDF（可选）**:
  - 若已安装 librsvg: `rsvg-convert -w 2480 -h 3508 input.svg -o output.png`
  - 若已安装 Inkscape: `inkscape input.svg --export-type=png --export-filename=output.png`
  - PDF: 多数设计工具或浏览器打印面板可直接导出为 PDF

#### 占位符键（在 SVG 内以 {{KEY}} 形式出现）
- **TITLE**: 主标题
- **SUBTITLE**: 副标题或短句
- **DATE**: 日期（如 2025-09-15）
- **TIME**: 时间（如 14:00 - 16:00）
- **LOCATION**: 地点
- **CTA**: 号召性用语（如 立即报名）
- **WEBSITE**: 网站或品牌文案
- **QR_TEXT**: 二维码下方说明
- **TAGLINE**: 品牌口号
- **SPONSOR**: 主办/赞助
- **CONTACT**: 联系方式
- **PHOTO**: 图片（支持本地路径；渲染脚本会自动内嵌为 data URI）

#### 尺寸
- **A4 竖版**: 2480 × 3508 px（300 DPI 打印友好）
- **社交竖版**: 1080 × 1920 px（适合朋友圈/视频号/故事）

#### 文件列表
- `poster-minimal-a4.svg`: 极简风 A4
- `poster-gradient-a4.svg`: 渐变色块 A4
- `poster-brand-leftbar-a4.svg`: 品牌左侧色条 A4
- `poster-geometry-a4.svg`: 几何装饰 A4
- `poster-photo-1080x1920.svg`: 顶部大图社交海报
- `sample-data.json`: 示例数据（可复制后修改）
- `render_posters.py`: 批量渲染脚本

#### 小贴士
- 字体使用系统无衬线字体回退链（如 Inter/Arial/Helvetica/sans-serif）。如需品牌字重，请在设计软件替换。
- 颜色、圆角、装饰图形均为 SVG 可编辑对象，可直接在文件中调整 `fill`、`stroke` 等属性。