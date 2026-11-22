'use strict';
// Small, deterministic, accessible progressive enhancements (no dependencies).
document.addEventListener('DOMContentLoaded', () => {
  const search = document.getElementById('chapter-search');
  if (search) {
    const count = document.getElementById('search-count');
    search.addEventListener('input', () => {
      const needle = search.value.trim().toLocaleLowerCase();
      let shown = 0;
      document.querySelectorAll('.chapter-card').forEach(card => {
        const hit = card.textContent.toLocaleLowerCase().includes(needle);
        card.hidden = !hit;
        if (hit) shown++;
      });
      if (count) count.textContent = needle ? '找到 ' + shown + ' 篇' : '';
    });
  }

  const range = document.getElementById('chunk-window-size');
  const sizeLabel = document.getElementById('window-size-label');
  if (range && sizeLabel) {
    range.addEventListener('input', () => {
      sizeLabel.textContent = range.value;
    });
  }

  const demo = {
    boundary: () => '去掉检索来源后，答案无可验证依据；加入版本与出处后，才可以核对「2026版·7天」的声明。RAG 仍可能误引，不能保证事实正确。',
    budget: () => {
      const W = 8192, S = 500, O = 1500, Q = 300;
      return '示例预算：8192 − 500（系统指令）− 1500（预留输出）− 300（问题）= ' +
        (W-S-O-Q) + ' token 可用于检索上下文。实际应使用对应模型 tokenizer 计数。';
    },
    ranking: () => '演示查询「退款期」：D2（包含 7 天退款）→ D1（仅谈付款）→ D3（无关文档）。排序仅展示玩具词项匹配，不等于向量检索结果。',
    'parse-table': () => '结构化结果：行键=收入；列名=2026年；数值=9；单位=万元。可回链到原表格的位置。此例只是字段级展示。',
    'chunk-preview': () => {
      const chars = Array.from('2026版购买后7天内可退款');
      const size = range ? Number(range.value) : 10;
      const overlap = 3;
      const windows = [];
      for (let start = 0; start < chars.length;) {
        const end = Math.min(start + size, chars.length);
        windows.push('[' + start + ',' + end + '): ' + chars.slice(start, end).join(''));
        if (end === chars.length) break;
        start = end - overlap;
      }
      return '字符窗口 size=' + size + ', overlap=3：' + windows.join('  |  ') +
        '。仅按字符滑动，不是 tokenizer。';
    },
    'bm25-saturation': () => {
      const k1 = 1.2;
      const f = t => t * (k1 + 1) / (t + k1);
      const rows = [1, 5, 10].map(t => 'tf=' + t + ' → 贡献 ' + f(t).toFixed(2));
      return '取 k1=1.2，并令 |D|=avgdl（长度因子=1）：' + rows.join('；') +
        '。上界为 k1+1=2.2，出现次数再多也只趋近它，不会线性增长。';
    },
    'ann-recall': () => {
      const total = 400;
      const rows = [[1, 62, 0.46], [2, 128, 0.71], [4, 246, 0.88], [8, 400, 1.0]];
      return '玩具 IVF（教学示意，非实测）：' + rows.map(r =>
        'nprobe=' + r[0] + ' → 扫描 ' + r[1] + '/' + total + '，recall@5≈' + r[2].toFixed(2)
      ).join('；') + '。nprobe 增大时扫描量与召回同时上升，实际以你的数据实测为准。';
    },
    'vector-geometry': () => {
      const a = [0.9, 0.1], b = [3, 3];
      const dotA = a[0], dotB = b[0];
      const cosA = dotA / Math.hypot(...a), cosB = dotB / Math.hypot(...b);
      return '点积：D1=' + dotA.toFixed(3) + '，D2=' + dotB.toFixed(3) +
        ' → D2 较高；余弦：D1=' + cosA.toFixed(3) + '，D2=' + cosB.toFixed(3) +
        ' → D1 较高。数值来自人为指定的二维向量。';
    }
  };
  document.querySelectorAll('button[data-demo]').forEach(button => {
    button.addEventListener('click', () => {
      const out = document.getElementById(button.getAttribute('aria-controls'));
      const render = demo[button.dataset.demo];
      if (out && render) out.textContent = render();
    });
  });
});
