/* diagram.js — render a validated maths diagram spec (from /api/diagram) into
   exact SVG. The model only describes the figure; this draws it correctly.
   window.renderDiagram(spec) -> SVG string ('' if nothing to draw). */
(function () {
  'use strict';

  const ACCENT = '#7C3AED', ACCENT2 = '#3B82F6', FILL = 'rgba(124,58,237,.20)';
  const INK = 'style="fill:var(--text,#1e1b2e)"';        // theme-aware text
  const MUT = 'style="fill:var(--text-muted,#6b7280)"';

  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const fmt = n => { const r = Math.round(n * 1000) / 1000; return Math.abs(r - Math.round(r)) < 1e-9 ? String(Math.round(r)) : String(r); };
  const svg = (w, h, body) =>
    `<svg viewBox="0 0 ${w} ${h}" style="width:100%;max-width:${w}px;height:auto;font-family:var(--font,sans-serif);font-weight:700" role="img">${body}</svg>`;

  function numberLine(s) {
    const W = 320, H = 72, x0 = 22, x1 = 298, y = 40;
    const map = v => x0 + (v - s.min) / (s.max - s.min) * (x1 - x0);
    let b = `<line x1="${x0-8}" y1="${y}" x2="${x1+8}" y2="${y}" stroke="${ACCENT}" stroke-width="2.5"/>`;
    b += `<polygon points="${x1+8},${y} ${x1+1},${y-4} ${x1+1},${y+4}" fill="${ACCENT}"/>`;
    b += `<polygon points="${x0-8},${y} ${x0-1},${y-4} ${x0-1},${y+4}" fill="${ACCENT}"/>`;
    for (let v = s.min; v <= s.max + 1e-9; v += s.step) {
      const x = map(v);
      b += `<line x1="${x}" y1="${y-5}" x2="${x}" y2="${y+5}" stroke="${ACCENT}" stroke-width="1.5"/>`;
      b += `<text x="${x}" y="${y+20}" text-anchor="middle" font-size="11" ${MUT}>${esc(fmt(v))}</text>`;
    }
    (s.points || []).forEach(p => {
      const x = map(p.value);
      b += `<circle cx="${x}" cy="${y}" r="5.5" fill="${ACCENT2}" stroke="#fff" stroke-width="2"/>`;
      if (p.label) b += `<text x="${x}" y="${y-12}" text-anchor="middle" font-size="11" ${INK}>${esc(p.label)}</text>`;
    });
    return svg(W, H, b);
  }

  function fractionBar(s) {
    const x0 = 14, bw = 250, rh = 34, gap = 12;
    const H = s.fractions.length * (rh + gap) + 6;
    let b = '';
    s.fractions.forEach((f, i) => {
      const y = i * (rh + gap) + 4, cw = bw / f.denominator;
      for (let k = 0; k < f.denominator; k++) {
        b += `<rect x="${x0 + k*cw}" y="${y}" width="${cw}" height="${rh}" fill="${k < f.numerator ? FILL : 'transparent'}" stroke="${ACCENT}" stroke-width="1.5"/>`;
      }
      b += `<text x="${x0 + bw + 12}" y="${y + rh/2 + 5}" font-size="16" ${INK}>${f.numerator}/${f.denominator}${f.label ? ' ' + esc(f.label) : ''}</text>`;
    });
    return svg(320, H, b);
  }

  function barChart(s) {
    const W = 320, H = 190, base = 150, x0 = 30, top = s.title ? 28 : 10;
    const max = Math.max(...s.bars.map(b => b.value)) || 1;
    const slot = (W - x0 - 12) / s.bars.length, bw = Math.min(slot * 0.62, 46);
    let b = s.title ? `<text x="${W/2}" y="16" text-anchor="middle" font-size="13" ${INK}>${esc(s.title)}</text>` : '';
    b += `<line x1="${x0}" y1="${base}" x2="${W-8}" y2="${base}" stroke="var(--text-muted,#9ca3af)" stroke-width="1.5"/>`;
    s.bars.forEach((bar, i) => {
      const h = (bar.value / max) * (base - top - 14);
      const x = x0 + i * slot + (slot - bw) / 2, y = base - h;
      b += `<rect x="${x}" y="${y}" width="${bw}" height="${h}" rx="3" fill="${ACCENT}"/>`;
      b += `<text x="${x+bw/2}" y="${y-4}" text-anchor="middle" font-size="11" ${INK}>${esc(fmt(bar.value))}</text>`;
      b += `<text x="${x+bw/2}" y="${base+15}" text-anchor="middle" font-size="10.5" ${MUT}>${esc(bar.label)}</text>`;
    });
    return svg(W, H, b);
  }

  function rectangle(s) {
    const maxw = 240, maxh = 150, sc = Math.min(maxw / s.width, maxh / s.height);
    const w = s.width * sc, h = s.height * sc, x = 40, y = 16, u = s.unit ? ' ' + esc(s.unit) : '';
    let b = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${FILL}" stroke="${ACCENT}" stroke-width="2.5"/>`;
    b += `<text x="${x + w/2}" y="${y + h + 20}" text-anchor="middle" font-size="13" ${INK}>${fmt(s.width)}${u}</text>`;
    b += `<text x="${x - 10}" y="${y + h/2 + 4}" text-anchor="end" font-size="13" ${INK}>${fmt(s.height)}${u}</text>`;
    b += `<text x="${x + w/2}" y="${y + h/2 + 5}" text-anchor="middle" font-size="12" ${MUT}>Area ${fmt(s.width*s.height)}${u ? u+'²' : ''}</text>`;
    return svg(maxw + 80, maxh + 40, b);
  }

  function rightTriangle(s) {
    const maxw = 220, maxh = 150, sc = Math.min(maxw / s.base, maxh / s.height);
    const bw = s.base * sc, bh = s.height * sc, ox = 44, oy = 16;
    const A = [ox, oy + bh], B = [ox + bw, oy + bh], Cp = [ox, oy];  // right angle at A
    const u = s.unit ? ' ' + esc(s.unit) : '', hyp = Math.sqrt(s.base*s.base + s.height*s.height);
    let b = `<polygon points="${A} ${B} ${Cp}" fill="${FILL}" stroke="${ACCENT}" stroke-width="2.5"/>`;
    b += `<path d="M ${A[0]} ${A[1]-14} h 14 v 14" fill="none" stroke="${ACCENT}" stroke-width="1.5"/>`;  // right-angle mark
    b += `<text x="${ox + bw/2}" y="${oy + bh + 20}" text-anchor="middle" font-size="13" ${INK}>${fmt(s.base)}${u}</text>`;
    b += `<text x="${ox - 10}" y="${oy + bh/2 + 4}" text-anchor="end" font-size="13" ${INK}>${fmt(s.height)}${u}</text>`;
    b += `<text x="${ox + bw/2 + 10}" y="${oy + bh/2}" font-size="12" ${MUT}>${fmt(hyp)}${u}</text>`;
    return svg(maxw + 80, maxh + 40, b);
  }

  function compile(expr) {
    if (!/^[0-9xX+\-*/^(). ]+$/.test(expr)) return null;
    const js = expr.replace(/\^/g, '**').replace(/X/g, 'x');
    try { const f = new Function('x', 'return (' + js + ');'); f(1); return f; } catch (e) { return null; }
  }

  function functionPlot(s) {
    const f = compile(s.expression); if (!f) return '';
    const W = 320, H = 220, pad = 26, N = 120;
    const xs = [], ys = [];
    for (let i = 0; i <= N; i++) {
      const x = s.xmin + (s.xmax - s.xmin) * i / N, y = Number(f(x));
      if (Number.isFinite(y)) { xs.push(x); ys.push(y); }
    }
    if (ys.length < 2) return '';
    let ymin = Math.min(...ys), ymax = Math.max(...ys);
    if (ymin === ymax) { ymin -= 1; ymax += 1; }
    const padY = (ymax - ymin) * 0.1; ymin -= padY; ymax += padY;
    const mx = x => pad + (x - s.xmin) / (s.xmax - s.xmin) * (W - 2*pad);
    const my = y => H - pad - (y - ymin) / (ymax - ymin) * (H - 2*pad);
    let b = `<rect x="${pad}" y="${pad}" width="${W-2*pad}" height="${H-2*pad}" fill="none" stroke="var(--border,#e5e7eb)" stroke-width="1"/>`;
    if (s.xmin < 0 && s.xmax > 0) b += `<line x1="${mx(0)}" y1="${pad}" x2="${mx(0)}" y2="${H-pad}" stroke="var(--text-muted,#9ca3af)" stroke-width="1"/>`;
    if (ymin < 0 && ymax > 0) b += `<line x1="${pad}" y1="${my(0)}" x2="${W-pad}" y2="${my(0)}" stroke="var(--text-muted,#9ca3af)" stroke-width="1"/>`;
    const pts = xs.map((x, i) => `${mx(x).toFixed(1)},${my(ys[i]).toFixed(1)}`).join(' ');
    b += `<polyline points="${pts}" fill="none" stroke="${ACCENT}" stroke-width="2.5" stroke-linejoin="round"/>`;
    b += `<text x="${W-pad}" y="${pad-8}" text-anchor="end" font-size="12" ${INK}>y = ${esc(s.expression)}</text>`;
    b += `<text x="${pad}" y="${H-6}" font-size="10" ${MUT}>x: ${fmt(s.xmin)}…${fmt(s.xmax)}</text>`;
    return svg(W, H, b);
  }

  // ── shared text helpers (science diagrams) ───────────────────────────────
  function wrap(text, maxChars) {
    const words = String(text).split(/\s+/), lines = []; let cur = '';
    words.forEach(w => {
      if ((cur + ' ' + w).trim().length <= maxChars) cur = (cur + ' ' + w).trim();
      else { if (cur) lines.push(cur); cur = w; }
    });
    if (cur) lines.push(cur);
    return lines.length ? lines : [''];
  }
  const tspans = (lines, x, y0, lh, attrs) =>
    lines.map((l, i) => `<text x="${x}" y="${(y0 + i*lh).toFixed(1)}" text-anchor="middle" ${attrs}>${esc(l)}</text>`).join('');

  function flow(s) {
    const steps = s.steps, N = steps.length, m = 8, aw = 16, fs = N > 4 ? 9 : 11;
    const bw = Math.max(54, (340 - 2*m - (N-1)*aw) / N);
    const cpl = Math.max(7, Math.floor(bw / (fs * 0.62)));
    const wr = steps.map(st => wrap(st.label, cpl));
    const maxL = Math.max(...wr.map(w => w.length));
    const bh = maxL * (fs + 3) + 14, top = 12, H = bh + 24;
    const W = 2*m + N*bw + (N-1)*aw;
    let b = '';
    steps.forEach((st, i) => {
      const x = m + i*(bw + aw), my = top + bh/2;
      b += `<rect x="${x}" y="${top}" width="${bw.toFixed(1)}" height="${bh}" rx="9" fill="${FILL}" stroke="${ACCENT}" stroke-width="2"/>`;
      const ty = my - ((wr[i].length - 1) * (fs+3)) / 2 + fs/2;
      b += tspans(wr[i], x + bw/2, ty, fs + 3, `font-size="${fs}" ${INK}`);
      if (i < N - 1) {
        const ax = x + bw, ax2 = ax + aw;
        b += `<line x1="${ax}" y1="${my}" x2="${ax2-4}" y2="${my}" stroke="${ACCENT}" stroke-width="2"/>`;
        b += `<polygon points="${ax2},${my} ${ax2-6},${my-4} ${ax2-6},${my+4}" fill="${ACCENT}"/>`;
      }
    });
    return svg(W, H, b);
  }

  function cycle(s) {
    const steps = s.steps, N = steps.length, W = 300, H = 280, cx = 150, cy = 140, r = 92, bw = 86, bh = 42;
    const node = i => { const a = -Math.PI/2 + i*2*Math.PI/N; return [cx + r*Math.cos(a), cy + r*Math.sin(a)]; };
    let b = '';
    for (let i = 0; i < N; i++) {                      // clockwise arrows (under boxes)
      const p = node(i), q = node((i+1) % N);
      const dx = q[0]-p[0], dy = q[1]-p[1], L = Math.hypot(dx, dy) || 1, ux = dx/L, uy = dy/L;
      const x1 = p[0]+ux*48, y1 = p[1]+uy*24, x2 = q[0]-ux*48, y2 = q[1]-uy*24;
      b += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${ACCENT2}" stroke-width="2"/>`;
      b += `<polygon points="${x2.toFixed(1)},${y2.toFixed(1)} ${(x2-ux*8-uy*4).toFixed(1)},${(y2-uy*8+ux*4).toFixed(1)} ${(x2-ux*8+uy*4).toFixed(1)},${(y2-uy*8-ux*4).toFixed(1)}" fill="${ACCENT2}"/>`;
    }
    for (let i = 0; i < N; i++) {
      const p = node(i), lines = wrap(steps[i].label, 13);
      b += `<rect x="${(p[0]-bw/2).toFixed(1)}" y="${(p[1]-bh/2).toFixed(1)}" width="${bw}" height="${bh}" rx="9" fill="${FILL}" stroke="${ACCENT}" stroke-width="2"/>`;
      b += tspans(lines, p[0], p[1] - ((lines.length-1)*12)/2 + 4, 12, `font-size="10.5" ${INK}`);
    }
    return svg(W, H, b);
  }

  function comparison(s) {
    const cols = s.columns, N = cols.length, m = 6, gap = 10, W = 340;
    const cw = (W - 2*m - (N-1)*gap) / N, hH = 28, ilH = 16, pad = 8;
    const wrapped = cols.map(c => c.items.map(it => wrap(it, Math.max(6, Math.floor(cw/6.2)))).flat());
    const maxLines = Math.max(1, ...wrapped.map(w => w.length));
    const bodyH = maxLines*ilH + pad*2, H = hH + 6 + bodyH + 8;
    let b = '';
    cols.forEach((c, i) => {
      const x = m + i*(cw + gap);
      b += `<rect x="${x.toFixed(1)}" y="2" width="${cw.toFixed(1)}" height="${hH}" rx="8" fill="${ACCENT}"/>`;
      b += `<text x="${(x+cw/2).toFixed(1)}" y="${2+hH/2+5}" text-anchor="middle" font-size="12.5" style="fill:#fff;font-weight:800">${esc(c.label)}</text>`;
      b += `<rect x="${x.toFixed(1)}" y="${hH+6}" width="${cw.toFixed(1)}" height="${bodyH}" rx="8" fill="none" stroke="var(--border,#d8d4e8)" stroke-width="1.5"/>`;
      wrapped[i].forEach((line, j) => {
        b += `<text x="${(x+cw/2).toFixed(1)}" y="${hH+6+pad+j*ilH+11}" text-anchor="middle" font-size="10.5" ${INK}>${esc(line)}</text>`;
      });
    });
    return svg(W, H, b);
  }

  window.renderDiagram = function (spec) {
    if (!spec || !spec.type) return '';
    try {
      switch (spec.type) {
        case 'number_line':   return numberLine(spec);
        case 'fraction_bar':  return fractionBar(spec);
        case 'bar_chart':     return barChart(spec);
        case 'rectangle':     return rectangle(spec);
        case 'right_triangle':return rightTriangle(spec);
        case 'function_plot': return functionPlot(spec);
        case 'cycle':         return cycle(spec);
        case 'flow':          return flow(spec);
        case 'comparison':    return comparison(spec);
        case 'image':         return spec.file
          ? `<img src="/api/media/${encodeURIComponent(spec.file)}" alt="" style="max-width:100%;max-height:260px">` : '';
      }
    } catch (e) {}
    return '';
  };
})();
