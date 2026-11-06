# 📎 RAG检索增强生成 · 从入门到精通

> 📘 28章 实战体系 · 交互式 HTML 课程

> **English TL;DR:** An all-Chinese 28-chapter course on **Retrieval-Augmented Generation (RAG)** — from the LLM pain points & three-stage evolution and the four-stage RAG architecture, through document parsing, chunking strategies (fixed/semantic/hierarchical/agentic), embeddings, vector databases (HNSW/IVF, ANN), sparse (BM25/SPLADE) vs dense (DPR), hybrid + RRF fusion, reranking (cross-encoder), and query rewriting (HyDE, step-back). Then generation & trust: citation, hallucination detection/fact-checking, safety guardrails & PII, privacy/access control. Advanced & frontier: RAG evaluation (RAGAS), multimodal RAG (CLIP), GraphRAG, Agentic RAG (LangGraph/ReAct), advanced indexing, LangChain vs LlamaIndex, vector-DB optimization, observability/OpenTelemetry, and frontier CRAG / Self-RAG / Speculative RAG — ending with a production deployment (Docker, scaling, semantic cache) and an end-to-end RAG capstone.

## 📖 课程简介

本课程系统构建 **RAG（检索增强生成）** 知识体系：从 LLM 痛点与 RAG 三阶段演进、四阶段架构讲起，覆盖文档解析、分块策略、Embedding 与向量数据库、稀疏（BM25/SPLADE）与稠密（DPR）检索、混合检索（RRF）与重排序、查询优化（HyDE/Step-Back）；随后进入信任与安全——引用溯源、幻觉检测、安全护栏、隐私权限，以及前沿的 GraphRAG、Agentic RAG、多模态 RAG 与 CRAG/Self-RAG/Speculative RAG，最后以生产部署（Docker/水平扩展/语义缓存）与端到端 RAG 项目实战收束。

## 🚀 快速开始

```bash
python3 -m http.server 8000   # 在项目根目录启动本地静态服务器
# 然后在浏览器打开 http://localhost:8000/
```

## 📂 项目结构

```text
rag-tutorial/
├── index.html / 01.html ~ 28.html / courses.json / theme.css
```

## 📖 章节分段

| 阶段 | 章节 | 核心 |
|------|------|------|
| **基础与架构** | 01–03 | 演进、LLM 基础、四阶段架构 |
| **索引与解析** | 04–07 | 文档解析、分块、Embedding、向量库 |
| **检索技术** | 08–13 | BM25、稠密检索、混合+RRF、重排、查询优化、上下文增强 |
| **信任与安全** | 14–18 | 生成/引用、幻觉检测、护栏、访问控制、评估 |
| **高级 RAG** | 19–23 | 多模态、GraphRAG、Agentic、高级索引、框架对比 |
| **生产与前沿** | 24–28 | 向量库选型、可观测、CRAG 等前沿、生产部署、端到端实战 |

## ✨ 亮点

- 覆盖 RAG 全链路：索引→检索→重排→生成→评估→部署
- 前沿全面：GraphRAG、Agentic RAG、Self-RAG/CRAG/Speculative
- 含生产级部署与端到端项目实战

## 🎯 前置知识

- 适合：RAG / LLM 应用工程师
- 建议具备：Python + 基础 LLM API 与检索概念

## ✨ 特色

- 从「为什么」到「怎么落地」再到「前沿反思」完整闭环
- 即开即用纯静态 HTML

---
*本课程由 `rag-tutorial/` 项目维护。*