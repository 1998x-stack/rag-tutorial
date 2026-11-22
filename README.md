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

**本轮完成：**第 01–03 篇的独立撰写、原生 SVG 图解、可操作的小实验、证据台账与系统设计改版。第 04–28 篇迁入统一网站目录，仍是旧版内容，尚未达到同等质量标准。

## 目录与发布

```text
site/                 # 可独立部署的静态站点（GitHub Pages 构建产物）
  index.html          # 课程首页
  chapters/01..28.html
  assets/css/         # 全局与文章 CSS
  assets/js/          # 无框架渐进增强脚本
  assets/figures/     # 原创可独立查看 SVG
content/legacy-notes/ # 原 docs/ 中 20 份编号不匹配的旧 Markdown 参考草稿
content/evidence/     # 前三篇的事实与文献台账
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

仓库含 `.github/workflows/pages.yml`，会尝试将 `site/` 作为静态站点构建输出部署。需要在 **Settings → Pages → Build and deployment** 中选 **GitHub Actions**。提交工作流不等于证明已上线；必须查看 Actions 成功记录和公开 URL。

## 重要边界

- 原始 RAG 模型来自 Lewis 等人 2020 年的具体研究；现代工程 RAG 不是该论文的唯一实现形式。
- 代码的玩具案例不应称为完整生产系统；所有评估指标需注明数据集和实验设置。
- `content/legacy-notes/` 只是历史资料，不是同编号 HTML 的规范源文件。
- 视觉设计参考 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts)，文字、图片与代码独立创作。
