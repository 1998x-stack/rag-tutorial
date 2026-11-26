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
    'mrr-hit': () => {
      const first = [1, 3, null];
      const mrr = first.reduce((s, r) => s + (r ? 1 / r : 0), 0) / first.length;
      const hit3 = first.filter(r => r && r <= 3).length / first.length;
      return '第一个相关文档名次 ' + first.map(r => r === null ? '未命中' : r).join(', ') +
        '：MRR = ' + mrr.toFixed(4) + '；Hit@3 = ' + hit3.toFixed(3) +
        '。只反映这三个给定名次，不代表任何真实系统。';
    },
    'clip-retrieval': () => {
      const q = [0.95, 0.30];
      const imgs = { '图A 装配示意': [0.90, 0.20], '图B 折线趋势': [0.10, 0.98], '图C 无关照片': [-0.80, 0.30] };
      const cos = (a, b) => (a[0] * b[0] + a[1] * b[1]) / (Math.hypot(...a) * Math.hypot(...b));
      const ranked = Object.keys(imgs).sort((x, y) => cos(q, imgs[y]) - cos(q, imgs[x]));
      return '文本向量与图库的余弦相似度：' + ranked.map(n => n + '=' + cos(q, imgs[n]).toFixed(3)).join('，') +
        '。向量是人为指定的二维坐标，不是任何模型的真实输出。';
    },
    'graph-multihop': () => {
      const triples = [
        ['张明', 'PARTICIPATES_IN', 'Alpha'], ['张明', 'PARTICIPATES_IN', 'Beta'],
        ['李芳', 'PARTICIPATES_IN', 'Alpha'], ['李芳', 'PARTICIPATES_IN', 'Gamma'],
        ['王强', 'PARTICIPATES_IN', 'Beta']
      ];
      const by = {};
      triples.forEach(([s, r, o]) => {
        if (r !== 'PARTICIPATES_IN') return;
        (by[s] = by[s] || new Set()).add(o);
      });
      const multi = Object.keys(by).filter(n => by[n].size > 1);
      const rows = Object.keys(by).map(n => n + ' 参与 ' + [...by[n]].join('、'));
      return rows.join('；') + '。同时参与多个项目的有：' + multi.join('、') +
        '。这是手写三元组上的集合运算，不是图数据库查询。';
    },
    'react-loop': () => {
      const tools = { vector: () => '文档：退货政策 7 天内可退', calc: () => '计算：7 - 3 = 4' };
      const choose = q => /[0-9]/.test(q) ? 'calc' : 'vector';
      const run = q => {
        const t = choose(q);
        return '第1步 行动=' + t + ' 观察=' + tools[t](q) + '；信息够了 → 生成答案（1/2 步）';
      };
      return '问“退货几天”：' + run('退货几天') + '；问“7 减 3 等于几”：' + run('7 减 3 等于几') +
        '。规则是写死的，不是模型决策；上限 2 步防止失控循环。';
    },
    'clearance-filter': () => {
      const LEVELS = ['public', 'internal', 'confidential', 'secret'];
      const docs = [['c1', 'public'], ['c2', 'internal'], ['c3', 'confidential']];
      const vis = level => docs.filter(d => LEVELS.indexOf(d[1]) <= LEVELS.indexOf(level))
        .map(d => d[0]).join(', ');
      return '外部访客(public) 可见: [' + vis('public') + ']；内部员工(internal) 可见: [' +
        vis('internal') + ']；管理员(secret) 可见: [' + vis('secret') +
        ']。不可见的分块根本不出现（默认拒绝）。';
    },
    'pii-mask': () => {
      const sample = '联系 james@company.com 或 13800001111，卡号 4111 1111 1111 1111。';
      const masked = sample
        .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, '<email已脱敏>')
        .replace(/1[3-9]\d{9}/g, '<phone已脱敏>')
        .replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '<card已脱敏>');
      return '正则脱敏后：' + masked + '（人名等无固定格式的实体不会被识别）';
    },
    'claim-split': () => {
      const answer = 'Transformer 的 self-attention 可以并行计算，且通过位置编码感知顺序。它的复杂度随序列长度平方增长。';
      const parts = answer.split(/[。；;]|，且|，并|，以及/).map(s => s.trim()).filter(Boolean);
      return '规则拆分出 ' + parts.length + ' 条声明：' + parts.map((c, i) => '声明' + (i + 1) + '：' + c).join('；') +
        '。这是按标点/连接词的规则拆分，不是语义拆分，仍需 NLI 或 LLM 判定。';
    },
    'citation-check': () => {
      const N = 3;
      const answer = '可并行计算[1]。位置编码提供顺序信息[2]。速度快了 5 倍[5]。';
      const cited = (answer.match(/\[(\d+)\]/g) || []).map(s => Number(s.slice(1, -1)));
      const valid = cited.filter(n => n >= 1 && n <= N);
      const invalid = cited.filter(n => n < 1 || n > N);
      return '出现编号 [' + cited.join(', ') + ']：合法 [' + valid.join(', ') +
        ']，越界 [' + invalid.join(', ') + ']（资料只给了 ' + N +
        ' 条）。校验器只查编号合法性，不判断内容是否被资料支持。';
    },
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
    'cosine-vs-dot': () => {
      const q = [0.9, 0.4];
      const docs = { D1: [1.0, 0.1], D2: [3.0, 3.0], D3: [-0.8, 0.6] };
      const norm = a => Math.hypot(a[0], a[1]);
      const cos = (a, b) => (a[0] * b[0] + a[1] * b[1]) / (norm(a) * norm(b));
      const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
      const names = Object.keys(docs);
      const by = f => [...names].sort((x, y) => f(q, docs[y]) - f(q, docs[x])).join(' > ');
      return '余弦排序：' + by(cos) + '；点积排序：' + by(dot) +
        '。点积把长向量 D2 抬到最前。数值来自人为指定的二维向量，不是模型输出。';
    },
    'position-weight': () => {
      const n = 5;
      const f = pos => {
        const x = pos / (n - 1);
        return 0.2 + 0.8 * Math.pow(2 * x - 1, 2);
      };
      const front = ['R', 'd2', 'd3', 'd4', 'd5'].indexOf('R');
      const mid = ['d2', 'd3', 'R', 'd4', 'd5'].indexOf('R');
      return '人为设定的 U 形权重：相关文档放最前 → 曝光度 ' + f(front).toFixed(2) +
        '；放中间 → ' + f(mid).toFixed(2) +
        '。权重是手写函数，不是模型实测的注意力；真实位置效应需在自己的模型上做消融。';
    },
    'query-expand': () => {
      const QUERY = '价格';
      const syn = { '价格': ['价格', '定价', '售价', '费用'] };
      const docs = ['X-200 电机的定价说明与采购流程', 'X-200 电机的安装步骤图解'];
      const hits = (doc, terms) => terms.filter(t => doc.includes(t));
      const rows = docs.map((d, i) =>
        '文档' + (i + 1) + '：原始命中 ' + hits(d, [QUERY]).length +
        ' 词，扩展后命中 ' + hits(d, syn[QUERY]).length + ' 词');
      return rows.join('；') + '。扩展把只出现“定价”的文档拉了回来；这是手工同义词表演示，不是 HyDE 或 LLM 改写。';
    },
    'toy-rerank': () => {
      const Q = '苹果公司2026年财务状况';
      const coarse = [
        '苹果公司的发展历史可以追溯到1976年',
        '2026年全球科技公司财务概览',
        '苹果公司2026年财务报告与利润披露',
        '香蕉的种植与营养价值'
      ];
      const overlap = d => {
        const qs = new Set(Q);
        let n = 0;
        for (const ch of qs) if (d.includes(ch)) n++;
        return n / qs.size;
      };
      const hasAll = d => (d.includes('苹果') && d.includes('财务')) ? 1 : 0;
      const score = d => overlap(d) + hasAll(d);
      const ranked = [...coarse].sort((a, b) => score(b) - score(a));
      return '粗排把「' + coarse[0] + '」放在首位；玩具重排后第一名是「' + ranked[0] +
        '」。重排只改变顺序，不改变候选集合；这是手写特征的演示，不是神经网络交叉编码器。';
    },
    'rrf-fusion': () => {
      const k = 60;
      const bm25 = ['doc_A', 'doc_B', 'doc_C'];
      const dense = ['doc_B', 'doc_D', 'doc_A'];
      const scores = {};
      [bm25, dense].forEach(list => list.forEach((id, i) => {
        scores[id] = (scores[id] || 0) + 1 / (k + i + 1);
      }));
      const ordered = Object.keys(scores).sort((a, b) =>
        scores[b] - scores[a] || (a < b ? -1 : 1));
      return 'RRF（k=60，名次从 1 开始）：' + ordered.map(id =>
        id + '=' + scores[id].toFixed(4)).join('，') +
        '。doc_B 在向量路第 1、BM25 路第 2，故最高；只在单路出现的 doc_C、doc_D 仍保留。';
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
      const rows = [[1, 100, 1.0], [2, 122, 1.0], [4, 232, 1.0], [8, 400, 1.0]];
      return '玩具 IVF（与本页 Python 示例相同的 seed=7 单查询）：' + rows.map(r =>
        'nprobe=' + r[0] + ' → 扫描 ' + r[1] + '/' + total + '，recall@5≈' + r[2].toFixed(2)
      ).join('；') + '。扫描量增大，但这个查询的召回已饱和；实际以你的数据实测为准。';
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
