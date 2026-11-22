# RAG 系统工程：从检索到可信生成

[在线课程](https://1998x-stack.github.io/rag-tutorial/) · [进入第一章](https://1998x-stack.github.io/rag-tutorial/01.html) · [贡献与规范](AGENTS.md)

这是一门中文、机制优先的 28 章 RAG 教程。与只列举框架名称的课程不同，教程逐步解释**离线索引、在线检索、证据筛选、可信生成与评估**的因果关系。

## 学习路线

| 阶段 | 章节 | 目标 |
|---|---|---|
| 基础认知 | 01–03 | RAG 的成立条件、模型边界与系统数据流 |
| 数据准备 | 04–07 | 解析、分块、向量与索引 |
| 检索增强 | 08–13 | BM25、Dense、Hybrid、Rerank、查询处理 |
| 可信生成 | 14–18 | 引用、幻觉分析、安全、权限、评估 |
| 扩展架构 | 19–23 | 多模态、GraphRAG、Agentic RAG |
| 工程落地 | 24–28 | 成本、监控、部署、项目实践 |

**已深度精修：**01–06 篇。第二批 04–06 分别深入了文档版面解析、分块机制和 Embedding 数学，新增 13 张原创 SVG、3 个可重复离线实验和证据台账。**07–28 篇**仍是沿用原站点的历史内容，尚未完成同等标准的逐章审查。

## 目录与发布

```text
site/                 # 可独立部署的静态站点（GitHub Pages 构建产物）
  index.html          # 课程首页
  chapters/01..28.html
  assets/css/         # 全局与文章 CSS
  assets/js/          # 无框架渐进增强脚本
  assets/figures/     # 原创可独立查看 SVG
content/legacy-notes/ # 原 docs/ 中 20 份编号不匹配的旧 Markdown 参考草稿
content/evidence/     # 01–06 章的事实与文献台账
examples/              # structured_ingest / chunking_lab / embedding_lab 等离线示例
scripts/check_site.py # 无外部依赖的基础结构测试
.github/workflows/    # 静态检查与 Pages 部署
AGENTS.md             # 后续代理/贡献者操作规约
```

为了保留旧链接，GitHub Pages 发布包内的 `01.html`–`28.html` 是章节跳转页。仓库根目录仍保留旧路径，网站首页会指向新站点。切换发布模式后，`https://1998x-stack.github.io/rag-tutorial/` 是规范入口。

## 本地预览

```bash
python3 -m http.server 8000
# 浏览 http://localhost:8000/site/
python3 scripts/check_site.py
```

## GitHub Pages

当前仓库使用 GitHub 自带的 **main 分支根目录 Pages 发布**；仓库根目录的 `index.html` 会跳转到 `site/index.html`，而 `site/` 是独立维护的标准静态站点。不要并行运行第二套部署流程。已观察到 2026-11-22 的分支 Pages 构建成功；公开 URL 是否可在当前网络打开仍需单独检查。

`.github/workflows/pages.yml` 作为**未来迁移到 GitHub Actions 发布源**的手动备选流程保留，不随每次 push 自动触发。只有将 Settings → Pages → Build and deployment 的 Source 切换为 GitHub Actions 后，才手动运行该工作流。此时输出路径为 `site/`，根目录自动成为新的课程首页。


## 第二批离线实验与质量门禁

```bash
python3 -m examples.structured_ingest
python3 -m examples.chunking_lab
python3 -m examples.embedding_lab
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
# 完整浏览器检查：pip install playwright && python -m playwright install chromium
python3 scripts/browser_check.py
```

- 示例分别演示 HTML 表格结构恢复、字符级分块与来源偏移、2D 人工向量相似度；**不是 OCR、真实语义向量模型或完整 RAG 生成服务**。
- [第二批事实审查与验收说明](content/reviews/indexing-foundations-04-06.md)。
- 交互及 SVG 均有无需 JavaScript 的默认说明；生产 RAG 还应结合授权、索引更新、标注数据与真实推理模型评估。
