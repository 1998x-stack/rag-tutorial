# 第二批审查记录：04–06 · 文档与索引基础

## 范围

- 04：多源解析，PDF 两栏、OCR 与原文阅读顺序，表格二维关系，版本与出处链路。
- 05：字符/token 计量区分、固定重叠窗口数学、父子检索、命题粒度、Contextual Retrieval 与 Late Chunking 的具体时序。
- 06：向量范数与评分、双编码器相容性、InfoNCE、ColBERT MaxSim、模型配置/索引迁移。

## 原站点的风险与处理

| 原有问题 | 本轮处理 |
|---|---|
| 文档抽取工具表按笼统“最快/最准”排序，旧示例 API 容易过时 | 换成按格式与布局失败类型选型，标明 Docling 示例为需安装的可选路径 |
| 表格示例将单位、列头与脚注混进无类型文本 | 用 row/column/unit/source 记录模型和独立 SVG 解释关系 |
| Markdown 旧稿以固定字符切块冒充固定 token 切块 | 严格声明 Python Unicode 代码点，与模型 tokenizer 分离 |
| 语义/Agentic/Contextual/Late Chunking 混用，宣传未经验证的 Recall 提升 | 逐一解释执行时序，引用论文与官方资料，不移植没有实验设置的具体增益数字 |
| Embedding 将语义相似等同事实正确，声称统一的最优模型和微调提升 | 从几何、任务损失与版本约束展开；不复用拼贴 MTEB 数字 |
| 将 BGE 系列的查询/文档前缀一概视为强制 | 改为依模型与 SDK 版本确定约定，拒绝编造通用的 prompt_name |

## 可复现演示

- `python3 -m examples.structured_ingest`：基本 HTML 表格结构/来源 ID；不是 PDF/OCR 引擎。
- `python3 -m examples.chunking_lab`：字符窗口、有效下标与父子块偏移；不运行 embedding。
- `python3 -m examples.embedding_lab`：手工 2D 向量点积/余弦、对比损失和 MaxSim；不是自然语言向量模型。
- `python3 -m unittest discover -s tests -v`：包括边界、稳定性、非法输入与评分方向。

## 发布验收

`python3 scripts/check_site.py` 验证内部路径、站点数量、SVG XML/说明、语义标签与证据台账。
`python3 scripts/browser_check.py` 通过 Playwright Chromium 测试首页和 01–06 章（1440、390、360 px），执行键盘按钮交互、图片解码、MathML 几何、横向溢出检查并输出截图报告。

当次实际 CI 执行结果以 Pull Request 的 Actions 记录为准；文档本身不宣称浏览器测试已经发生。

## 研究来源

- https://pypdf.readthedocs.io/en/stable/user/extract-text.html
- https://arxiv.org/abs/2408.09869
- https://www.anthropic.com/research/contextual-retrieval
- https://arxiv.org/abs/2409.04701
- https://aclanthology.org/2024.emnlp-main.845/
- https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html
- https://aclanthology.org/D19-1410/
- https://aclanthology.org/2020.emnlp-main.550/
- https://arxiv.org/abs/2004.12832
- https://arxiv.org/abs/2402.03216
- https://arxiv.org/abs/2506.05176
- https://developers.openai.com/api/docs/guides/embeddings
