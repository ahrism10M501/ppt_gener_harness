import fs from 'node:fs';
import { Resvg } from '@resvg/resvg-js';
import { mathjax } from 'mathjax-full/js/mathjax.js';
import { TeX } from 'mathjax-full/js/input/tex.js';
import { SVG } from 'mathjax-full/js/output/svg.js';
import { liteAdaptor } from 'mathjax-full/js/adaptors/liteAdaptor.js';
import { RegisterHTMLHandler } from 'mathjax-full/js/handlers/html.js';
import { AllPackages } from 'mathjax-full/js/input/tex/AllPackages.js';

const request = JSON.parse(fs.readFileSync(0, 'utf8'));
let svg;
let width = request.width;
if (request.mode === 'math') {
  const adaptor = liteAdaptor();
  RegisterHTMLHandler(adaptor);
  const document = mathjax.document('', {
    InputJax: new TeX({ packages: AllPackages.filter(x => !['html', 'require', 'autoload'].includes(x)) }),
    OutputJax: new SVG({ fontCache: 'none' }),
  });
  const node = document.convert(request.tex, { display: request.display });
  svg = adaptor.outerHTML(adaptor.firstChild(node));
  if (svg.includes('data-mjx-error')) throw new Error('Unsupported LaTeX: ' + request.tex);
  const viewbox = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
  width = Math.max(1, Math.ceil(viewbox[2] / 1000 * request.size / 72 * 300));
} else if (request.mode === 'svg') {
  svg = fs.readFileSync(request.input, 'utf8');
} else {
  throw new Error('Unknown render mode');
}
if (request.svg) fs.writeFileSync(request.svg, svg);
const image = new Resvg(svg, {
  fitTo: { mode: 'width', value: width },
  font: { defaultFontFamily: request.font, loadSystemFonts: true },
}).render();
fs.writeFileSync(request.output, image.asPng());
process.stdout.write(JSON.stringify({ width: image.width, height: image.height, dpi: 300 }));
