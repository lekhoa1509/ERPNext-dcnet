#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";
import { marked } from "marked";
import {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  HeadingLevel,
  ImageRun,
  PageBreak,
  PageNumber,
  Packer,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableOfContents,
  TableRow,
  TextRun,
  WidthType,
} from "docx";

const root = path.dirname(fileURLToPath(import.meta.url));
const htmlDir = path.join(root, "html");
const wordDir = path.join(root, "word");
const htmlAssetsDir = path.join(htmlDir, "assets");
const generatedDir = path.join(root, ".export-cache");

const modules = [
  {
    key: "dcnet-crm",
    title: "DCNET CRM",
    subtitle: "Quản lý bán hàng và chăm sóc khách hàng",
    source: "dcnet-crm/USER_GUIDE.md",
    overview: "crm-overview.svg",
    workflow: ["Tiềm năng", "Hoạt động", "Cơ hội", "Báo giá", "Đơn hàng", "Chăm sóc"],
  },
  {
    key: "dcnet-migrate",
    title: "DCNET Migrate",
    subtitle: "Import dữ liệu có kiểm soát",
    source: "dcnet-migrate/USER_GUIDE.md",
    overview: "migrate-workspace.svg",
    workflow: ["Backup", "Upload Excel", "Phân tích", "Kiểm tra trùng", "Duyệt kế hoạch", "Import", "Đối chiếu"],
  },
  {
    key: "dcnet-permission",
    title: "DCNET Permission",
    subtitle: "Phân quyền theo phòng ban và vai trò",
    source: "dcnet-permission/USER_GUIDE.md",
    overview: "permission-manager.svg",
    workflow: ["Yêu cầu quyền", "Chọn scope", "Gán user", "Cấp role", "Chặn module", "Test persona", "Áp dụng"],
  },
];

const escapeXml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

function workflowSvg(module) {
  const width = 1200;
  const height = 330;
  const count = module.workflow.length;
  const gap = 22;
  const margin = 48;
  const boxWidth = (width - margin * 2 - gap * (count - 1)) / count;
  const boxes = module.workflow.map((label, index) => {
    const x = margin + index * (boxWidth + gap);
    const nextX = x + boxWidth + gap;
    const arrow = index < count - 1
      ? `<line x1="${x + boxWidth}" y1="176" x2="${nextX - 8}" y2="176" stroke="#0f766e" stroke-width="4" marker-end="url(#arrow)"/>`
      : "";
    return `${arrow}<rect x="${x}" y="125" width="${boxWidth}" height="102" rx="14" fill="${index === count - 1 ? "#ccfbf1" : "#ffffff"}" stroke="#0f766e" stroke-width="2"/><circle cx="${x + 28}" cy="148" r="16" fill="#0f766e"/><text x="${x + 28}" y="154" text-anchor="middle" font-family="Arial" font-size="14" font-weight="700" fill="#fff">${index + 1}</text><text x="${x + boxWidth / 2}" y="184" text-anchor="middle" font-family="Arial" font-size="15" font-weight="700" fill="#164e63">${escapeXml(label)}</text>`;
  }).join("");
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#0f766e"/></marker></defs><rect width="${width}" height="${height}" rx="18" fill="#f0fdfa"/><text x="48" y="58" font-family="Arial" font-size="27" font-weight="700" fill="#134e4a">Quy trình training — ${escapeXml(module.title)}</text><text x="48" y="88" font-family="Arial" font-size="15" fill="#475569">Thực hiện từ trái sang phải; dừng và xác nhận khi dữ liệu hoặc quyền chưa đúng.</text>${boxes}<text x="48" y="290" font-family="Arial" font-size="13" fill="#64748b">Sơ đồ minh họa được sinh từ tài liệu training DCNET Flow.</text></svg>`;
}

const css = `
:root{--brand:#0f766e;--ink:#172b4d;--muted:#64748b;--line:#dbe3ea;--soft:#f0fdfa}
*{box-sizing:border-box}body{margin:0;background:#eef2f5;color:var(--ink);font:16px/1.65 Arial,"Segoe UI",sans-serif}
.topbar{position:sticky;top:0;z-index:5;background:#0f766e;color:#fff;padding:12px 24px;box-shadow:0 2px 10px #0002}.topbar a{color:#fff;text-decoration:none;font-weight:700}
.layout{max-width:1320px;margin:28px auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:26px;padding:0 18px}.toc{position:sticky;top:78px;align-self:start;max-height:calc(100vh - 100px);overflow:auto;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px}.toc strong{display:block;margin-bottom:10px}.toc a{display:block;color:#475569;text-decoration:none;padding:5px 0;font-size:14px}.toc a:hover{color:var(--brand)}
main{background:#fff;border:1px solid var(--line);border-radius:14px;padding:42px 54px;box-shadow:0 8px 30px #33415512}h1{font-size:34px;line-height:1.2;color:#134e4a;border-bottom:4px solid #99f6e4;padding-bottom:16px}h2{margin-top:42px;color:#115e59;border-left:5px solid #14b8a6;padding-left:13px}h3{color:#0f766e}p{margin:12px 0}blockquote{margin:18px 0;padding:12px 18px;border-left:5px solid #f59e0b;background:#fff7ed;color:#7c2d12}code{background:#f1f5f9;padding:2px 5px;border-radius:4px}pre{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;padding:18px;border-radius:10px;overflow:auto}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px}th{background:#0f766e;color:#fff;text-align:left}th,td{border:1px solid var(--line);padding:9px 11px;vertical-align:top}tr:nth-child(even) td{background:#f8fafc}img{display:block;max-width:100%;height:auto;margin:22px auto;border:1px solid var(--line);border-radius:10px}.caption{text-align:center;color:var(--muted);font-size:13px}.workflow{margin:24px 0}li{margin:5px 0}.meta{color:var(--muted)}footer{max-width:1320px;margin:0 auto 30px;text-align:center;color:var(--muted);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px;box-shadow:0 5px 18px #33415510}.card h2{margin-top:0;font-size:21px}.button{display:inline-block;background:#0f766e;color:#fff!important;text-decoration:none;padding:9px 14px;border-radius:7px}
@media(max-width:900px){.layout{display:block}.toc{position:relative;top:0;margin-bottom:20px}main{padding:28px 22px}}@media print{body{background:#fff}.topbar,.toc{display:none}.layout{display:block;margin:0;max-width:none}.layout main{border:0;box-shadow:none;padding:0}h2{break-before:auto;break-after:avoid}table,img{break-inside:avoid}}
`;

function makeToc(html) {
  const links = [];
  const body = html.replace(/<h2>(.*?)<\/h2>/g, (_, label) => {
    const id = label.replace(/<[^>]+>/g, "").replace(/[đĐ]/g, "d").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    links.push(`<a href="#${id}">${label.replace(/<[^>]+>/g, "")}</a>`);
    return `<h2 id="${id}">${label}</h2>`;
  });
  return { body, toc: links.join("") };
}

async function buildHtml(module, markdown) {
  const renderer = new marked.Renderer();
  renderer.image = ({ href, title, text }) => {
    const assetPath = href.replace(/^(?:\.\.\/)+assets\//, "");
    return `<img src="assets/${assetPath}" alt="${escapeXml(text)}"${title ? ` title="${escapeXml(title)}"` : ""}>`;
  };
  renderer.code = ({ text, lang }) => lang === "mermaid"
    ? `<figure class="workflow"><img src="assets/${module.key}-workflow.svg" alt="Sơ đồ quy trình ${escapeXml(module.title)}"><figcaption class="caption">Sơ đồ quy trình dùng trong training.</figcaption></figure>`
    : `<pre><code>${escapeXml(text)}</code></pre>`;
  marked.setOptions({ renderer, gfm: true });
  const parsed = marked.parse(markdown);
  const { body, toc } = makeToc(parsed);
  return `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeXml(module.title)} — Tài liệu training</title><link rel="stylesheet" href="assets/training.css"></head><body><div class="topbar"><a href="index.html">← Bộ tài liệu custom apps</a></div><div class="layout"><aside class="toc"><strong>Mục lục</strong>${toc}</aside><main>${body}</main></div><footer>DCNET Flow · Tài liệu training · Xuất ngày 13/07/2026</footer></body></html>`;
}

function plain(value) {
  return value.replace(/!\[[^\]]*\]\([^)]*\)/g, "").replace(/\[([^\]]+)\]\([^)]*\)/g, "$1").replace(/[*_~]/g, "").replace(/`([^`]+)`/g, "$1").replace(/<[^>]+>/g, "").trim();
}

function inlineRuns(value, options = {}) {
  const text = plain(value);
  return [new TextRun({ text, font: "Arial", size: 22, ...options })];
}

async function imageParagraph(imagePath, width = 640) {
  const png = await sharp(imagePath).png().toBuffer();
  const meta = await sharp(png).metadata();
  const height = Math.round(width * (meta.height / meta.width));
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 180, after: 180 }, children: [new ImageRun({ type: "png", data: png, transformation: { width, height }, altText: { title: "Hình minh họa", description: "Hình minh họa trong tài liệu training", name: path.basename(imagePath) } })] });
}

function parseTable(lines, start) {
  const rows = [];
  let index = start;
  while (index < lines.length && lines[index].trim().startsWith("|")) {
    const cells = lines[index].trim().replace(/^\||\|$/g, "").split("|").map((cell) => plain(cell.trim()));
    if (!cells.every((cell) => /^:?-{3,}:?$/.test(cell))) rows.push(cells);
    index += 1;
  }
  const tableRows = rows.map((cells, rowIndex) => new TableRow({
    tableHeader: rowIndex === 0,
    children: cells.map((cell) => new TableCell({
      shading: rowIndex === 0 ? { type: ShadingType.CLEAR, fill: "0F766E", color: "auto" } : undefined,
      margins: { top: 90, bottom: 90, left: 100, right: 100 },
      children: [new Paragraph({ children: inlineRuns(cell, rowIndex === 0 ? { bold: true, color: "FFFFFF" } : {}) })],
    })),
  }));
  return { element: new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: tableRows }), next: index };
}

async function markdownToDocxElements(module, markdown) {
  const lines = markdown.split(/\r?\n/);
  const elements = [];
  let paragraphBuffer = [];
  const flush = () => {
    if (!paragraphBuffer.length) return;
    elements.push(new Paragraph({ spacing: { after: 140, line: 330 }, children: inlineRuns(paragraphBuffer.join(" ")) }));
    paragraphBuffer = [];
  };
  for (let i = 0; i < lines.length;) {
    const line = lines[i];
    if (!line.trim()) { flush(); i += 1; continue; }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flush();
      const level = heading[1].length === 1 ? HeadingLevel.TITLE : heading[1].length === 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2;
      elements.push(new Paragraph({ heading: level, spacing: { before: heading[1].length === 1 ? 0 : 260, after: 140 }, children: inlineRuns(heading[2], { bold: true, color: heading[1].length === 1 ? "134E4A" : "0F766E", size: heading[1].length === 1 ? 38 : heading[1].length === 2 ? 30 : 25 }) }));
      i += 1; continue;
    }
    const image = line.match(/^!\[[^\]]*\]\(([^)]+)\)/);
    if (image) {
      flush();
      elements.push(await imageParagraph(path.resolve(path.dirname(path.join(root, module.source)), image[1])));
      i += 1; continue;
    }
    if (line.trim() === "```mermaid") {
      flush();
      while (i < lines.length && lines[i].trim() !== "```") i += 1;
      i += 1;
      elements.push(await imageParagraph(path.join(generatedDir, `${module.key}-workflow.svg`)));
      continue;
    }
    if (line.trim().startsWith("```")) {
      flush(); i += 1; const code = [];
      while (i < lines.length && lines[i].trim() !== "```") { code.push(lines[i]); i += 1; }
      i += 1;
      elements.push(new Paragraph({ shading: { type: ShadingType.CLEAR, fill: "F1F5F9", color: "auto" }, spacing: { before: 100, after: 140 }, children: [new TextRun({ text: code.join("\n"), font: "Courier New", size: 18 })] }));
      continue;
    }
    if (line.trim().startsWith("|")) {
      flush(); const parsed = parseTable(lines, i); elements.push(parsed.element); i = parsed.next; continue;
    }
    const list = line.match(/^\s*(?:[-*]|\d+\.)\s+(.+)$/);
    if (list) {
      flush();
      elements.push(new Paragraph({ bullet: { level: 0 }, spacing: { after: 70 }, children: inlineRuns(list[1]) }));
      i += 1; continue;
    }
    if (line.startsWith(">")) {
      flush();
      elements.push(new Paragraph({ indent: { left: 360 }, border: { left: { color: "F59E0B", size: 18, style: BorderStyle.SINGLE, space: 10 } }, shading: { type: ShadingType.CLEAR, fill: "FFF7ED", color: "auto" }, spacing: { before: 100, after: 120 }, children: inlineRuns(line.replace(/^>\s?/, ""), { color: "7C2D12", italics: true }) }));
      i += 1; continue;
    }
    if (/^---+$/.test(line.trim())) { flush(); i += 1; continue; }
    paragraphBuffer.push(line.trim()); i += 1;
  }
  flush();
  return elements;
}

function makeDocument(children, title) {
  return new Document({
    creator: "DCNET Team",
    title,
    description: "Tài liệu training các chức năng custom DCNET Flow",
    styles: { default: { document: { run: { font: "Arial", size: 22, color: "172B4D" }, paragraph: { spacing: { line: 330 } } } } },
    sections: [{
      properties: { page: { margin: { top: 900, right: 850, bottom: 850, left: 850 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "DCNET Flow · Tài liệu training · Trang ", color: "64748B", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], color: "64748B", size: 18 })] })] }) },
      children: [new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-2" }), new Paragraph({ children: [new PageBreak()] }), ...children],
    }],
  });
}

await fs.rm(htmlDir, { recursive: true, force: true });
await fs.rm(wordDir, { recursive: true, force: true });
await fs.rm(generatedDir, { recursive: true, force: true });
await fs.mkdir(htmlAssetsDir, { recursive: true });
await fs.mkdir(wordDir, { recursive: true });
await fs.mkdir(generatedDir, { recursive: true });
await fs.writeFile(path.join(htmlAssetsDir, "training.css"), css);

await fs.cp(path.join(root, "assets"), htmlAssetsDir, { recursive: true });

const combinedElements = [];
for (const [index, module] of modules.entries()) {
  const markdown = await fs.readFile(path.join(root, module.source), "utf8");
  const svg = workflowSvg(module);
  const workflowPath = path.join(generatedDir, `${module.key}-workflow.svg`);
  await fs.writeFile(workflowPath, svg);
  await fs.writeFile(path.join(htmlAssetsDir, `${module.key}-workflow.svg`), svg);
  await fs.writeFile(path.join(htmlDir, `${module.key}.html`), await buildHtml(module, markdown));
  const elements = await markdownToDocxElements(module, markdown);
  const individual = makeDocument(elements, `Hướng dẫn ${module.title}`);
  await fs.writeFile(path.join(wordDir, `${module.key}-USER-GUIDE.docx`), await Packer.toBuffer(individual));
  if (index) combinedElements.push(new Paragraph({ children: [new PageBreak()] }));
  combinedElements.push(...elements);
}

const indexCards = modules.map((module) => `<article class="card"><h2>${escapeXml(module.title)}</h2><p>${escapeXml(module.subtitle)}</p><img src="assets/${module.overview}" alt="Minh họa ${escapeXml(module.title)}"><p><a class="button" href="${module.key}.html">Mở tài liệu chi tiết</a></p></article>`).join("");
await fs.writeFile(path.join(htmlDir, "index.html"), `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DCNET Flow — Bộ tài liệu training custom apps</title><link rel="stylesheet" href="assets/training.css"></head><body><div class="topbar">DCNET Flow · Bộ tài liệu training custom apps</div><div class="layout" style="display:block;max-width:1180px"><main><h1>Bộ tài liệu training các chức năng custom</h1><p class="meta">Bản HTML chạy offline · Cập nhật 13/07/2026</p><div class="cards">${indexCards}</div></main></div><footer>DCNET Team · 2026</footer></body></html>`);

await fs.writeFile(path.join(wordDir, "DCNET-CUSTOM-APPS-TRAINING.docx"), await Packer.toBuffer(makeDocument(combinedElements, "DCNET Custom Apps Training")));
await fs.rm(generatedDir, { recursive: true, force: true });

console.log(`Đã tạo ${modules.length + 1} file HTML và ${modules.length + 1} file Word.`);
