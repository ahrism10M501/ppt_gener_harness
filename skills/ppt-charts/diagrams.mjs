// Local SVG rendering; keep browser CSS and remote font imports out of PPT assets.
import fs from 'node:fs';
import { renderMermaidSVG } from 'beautiful-mermaid';
import { Resvg } from '@resvg/resvg-js';

const request = JSON.parse(fs.readFileSync(0, 'utf8'));
const p = request.palette;
const hex = key => `#${p[key]}`;
// Blend toward the slide background, not white, so dark presets keep light labels readable.
const tint = (key, weight) => {
  const value = p[key];
  return '#' + [0, 2, 4].map(i => Math.round(
    parseInt(value.slice(i, i + 2), 16) * weight + parseInt(p.background.slice(i, i + 2), 16) * (1 - weight),
  ).toString(16).padStart(2, '0')).join('');
};
const colors = {
  bg: hex('background'), fg: hex('text'), line: hex('secondary'),
  accent: hex('primary'), muted: hex('band'),
  surface: tint('primary', 0.06), border: tint('primary', 0.45),
};
let code = request.code;
if (/^(?:graph|flowchart)\b/.test(code.trim())) {
  code += `\nclassDef focus fill:${hex('primary')},stroke:${hex('band')},color:${hex('background')},stroke-width:2px`;
}
let svg = renderMermaidSVG(code, {
  ...colors, font: request.font, padding: 16, nodeSpacing: 26, layerSpacing: 26,
});

// resvg does not implement CSS custom properties or color-mix().
const fixed = {
  ...colors, _text: colors.fg, '_text-sec': colors.muted,
  '_text-muted': colors.muted, '_text-faint': tint('text', 0.4),
  _line: colors.line, _arrow: colors.accent,
  '_node-fill': colors.surface, '_node-stroke': colors.border,
  '_group-fill': colors.bg, '_group-hdr': tint('primary', 0.1),
  '_inner-stroke': colors.border, '_key-badge': tint('primary', 0.12),
};
svg = svg.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, '')
  .replace(/\sstyle="--bg:[^"]*"/, '')
  .replace(/var\(--([\w-]+)\)/g, (_, key) => {
    if (!(key in fixed)) throw new Error(`Unknown renderer color: ${key}`);
    return fixed[key];
  });
const family = request.font.replaceAll('&', '&amp;').replaceAll('"', '&quot;');
svg = svg.replace('<svg ', `<svg font-family="${family}" `);
// A real background rect also works in SVG viewers that ignore CSS backgrounds.
svg = svg.replace(/(<svg\b[^>]*>)/, `$1<rect width="100%" height="100%" fill="${colors.bg}"/>`);
if (/@import|var\(|color-mix\(|<foreignObject|<script/i.test(svg)) {
  throw new Error('SVG contains unsupported or non-local content');
}
fs.writeFileSync(request.svg, svg);
const rendered = new Resvg(svg, {
  fitTo: { mode: 'width', value: request.width },
  font: { defaultFontFamily: request.font, loadSystemFonts: true },
}).render();
fs.writeFileSync(request.png, rendered.asPng());
