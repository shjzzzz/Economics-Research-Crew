---
type: index
updated: YYYY-MM-DD
---

# Index（文件系统与知识系统总路由）

> 由 `/ingest-source`、`/wiki-lint` 维护：本文件同时路由**文件系统**（目录位置与读写边界）与**知识系统**（双链图谱与内容目录）。每次知识库整理须同步更新本文件与 `Meta/log.md`。

## 一、文件系统路由（目录位置与边界）
> 实时目录树见 `Meta/folder-map.md`，完整四层架构与权限规则见 `Meta/vault-map.md`，变更日志见 `Meta/log.md`。

| 物理路径 | 层级 | 用途与定位方式 | 读写约束 |
|---|---|---|---|
| `03-Literature/_sources/` | Tier 0 | 论文 PDF、法规原文、OCR 稿等原始来源 | **只读不可变**（hook 保护） |
| `06-Data/raw/` | Tier 0 | 原始数据集 | **只读不可变**（hook 保护） |
| 根目录既有笔记 | Tier 0 | 既有文献库/知识库笔记，按目录检索 | **保持原位**，不进双链图 |
| `02-Areas/` | Tier 1 | 长期职责与主题领域页 | 跨项目复用，进知识路由与 lint |
| `00-Inbox/` | 暂存 | 待整理或待评估的临时材料 | 整理后分流或留存 |
| `01-Research-Projects/<项目>/` | Tier 2 | `PROJECT.md`、`STATE.json`、`analysis-plan.md`、`paper/` | 仅 `PROJECT.md` 进下方知识路由 |
| `06-Data/{processed,metadata}/` | Tier 2 | 清洗后的衍生数据与数据字典 | 衍生写入 |
| `07-Code/{stata,python,R}/` | Tier 2 | 实证与绘图脚本 | 模块化可复现 |
| `09-Writing/` & `10-Archive/` | Tier 3 | 独立文稿（简报/讲义）与结项归档 | 不放活跃项目过程稿 |
| `Meta/` | 控制面 | 规范（`purpose`/`decisions`/`vault-map`）、账本（`index`/`log`/`source-registry`/`review-queue`/`constraints`/`aliases`）、地图（`folder-map`/`link-map`） | 机读 JSON/JSONL 由脚本独占 |

---

## 二、知识系统路由（双链图谱与内容目录）
> 回答问题时先读本区与 `Meta/link-map.md` 枢纽页，再沿 `[[双链]]` 展开；每页一行，`[[页面]]` + 一句话摘要。收录 Tier 1 跨项目知识页、Tier 2 项目入口页（`PROJECT.md`）与 `09-Writing/` 独立文稿。

### 主题枢纽（MOC）
| 页面 | 主题范围 | 更新 |
|---|---|---|

### 文献（03-Literature）
| 页面 | 摘要 | cite_key | 来源数 | 更新 |
|---|---|---|---|---|

### 理论与机制（04-Theories）
| 页面 | 摘要 | 来源数 | 更新 |
|---|---|---|---|

### 方法与识别（05-Methods）
| 页面 | 摘要 | 来源数 | 更新 |
|---|---|---|---|

### 研究项目入口（01-Research-Projects）
| 页面 | 研究问题与当前阶段 | 状态 | 更新 |
|---|---|---|---|

### 研究笔记与综合（08-Research-Notes）
| 页面 | 摘要 | 类型（synthesis / query） | 更新 |
|---|---|---|---|

### 独立文稿（09-Writing）
| 页面 | 用途（政策简报 / 评论 / 讲义等） | 更新 |
|---|---|---|
