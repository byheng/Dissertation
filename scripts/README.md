# BibTeX 文献查询工具

本目录提供两个 BibTeX 查询工具，用于自动获取学术文献的标准引用格式。

## 🌟 推荐工具：CrossRef 查询 (fetch_bibtex_crossref.py)

**优先使用此工具**，具有以下优势：
- ✅ 无需科学上网
- ✅ 无反爬虫限制
- ✅ 速度快且稳定
- ✅ 数据权威（来自出版社）
- ✅ 无需安装额外依赖（仅需 `requests`）

### 安装依赖

```bash
# 通常系统已自带 requests 库，如果没有：
pip3 install requests
```

### 使用方法

**基本用法：**

```bash
python3 fetch_bibtex_crossref.py "文献标题"
```

**示例 1：查询 ORB-SLAM 论文**

```bash
python3 fetch_bibtex_crossref.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"
```

输出：
```bibtex
@article{Mur_Artal_2015,
  title={ORB-SLAM: A Versatile and Accurate Monocular SLAM System},
  volume={31},
  DOI={10.1109/tro.2015.2463671},
  number={5},
  journal={IEEE Transactions on Robotics},
  author={Mur-Artal, Raul and Montiel, J. M. M. and Tardos, Juan D.},
  year={2015},
  pages={1147–1163}
}
```

**示例 2：查询会议论文**

```bash
python3 fetch_bibtex_crossref.py "DTAM: Dense tracking and mapping in real-time"
```

**示例 3：使用 DOI 直接查询（最快最准确）**

```bash
python3 fetch_bibtex_crossref.py --doi "10.1109/TRO.2015.2463671"
```

**示例 4：保存到文件**

```bash
python3 fetch_bibtex_crossref.py "VINS-Mono" -o vins.bib
```

**示例 5：直接添加到项目 ref.bib**

```bash
python3 fetch_bibtex_crossref.py "Visual SLAM Survey" >> ../Biblio/ref.bib
```

### CrossRef 工具参数

- `title`：文献标题（可选，如果提供 --doi 则不需要）
- `--doi`：直接使用 DOI 查询（例如：10.1109/TRO.2015.2463671）
- `-o, --output`：输出到指定文件

### 注意事项

- 仅支持有 DOI 的文献（大多数学术论文都有）
- 对于期刊论文和会议论文效果最好
- arXiv 预印本可能没有 DOI，建议使用谷歌学术工具

---

## 📚 备选工具：谷歌学术查询 (fetch_bibtex.py)

当 CrossRef 找不到文献时（如 arXiv 预印本、技术报告等），可使用此工具。

### 安装依赖

```bash
pip3 install scholarly
```

或使用 requirements.txt：

```bash
pip3 install -r requirements.txt
```

### 使用方法

**基本用法：**

```bash
python3 fetch_bibtex.py "文献标题"
```

**示例 1：查询论文**

```bash
python3 fetch_bibtex.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"
```

**示例 2：使用免费代理（当遇到反爬虫限制时）**

```bash
python3 fetch_bibtex.py --proxy "Visual SLAM: A Survey"
```

**示例 3：使用 Selenium 模式（需要 Chrome 浏览器）**

```bash
python3 fetch_bibtex.py --selenium "SLAM Survey"
```

### 谷歌学术工具参数

- `title`（必需）：文献标题
- `-o, --output`：输出到指定文件
- `--proxy`：使用免费代理
- `--selenium`：使用 Selenium 模式（需要 Chrome）
- `--retry`：重试次数（默认 3）

### 注意事项

1. **查询频率限制**：谷歌学术有反爬虫机制，建议：
   - 两次查询之间间隔至少 3-5 秒
   - 如遇封禁，使用 `--proxy` 或 `--selenium` 选项
   - 或稍后重试

2. **网络要求**：
   - 需要能够访问谷歌学术（国内用户需要科学上网）
   - 确保网络连接稳定

3. **优先使用 CrossRef**：
   - 对于有 DOI 的论文，强烈推荐使用 CrossRef 工具
   - 谷歌学术工具仅作为备选方案

---

## 🚀 快速开始指南

### 推荐工作流程

1. **首选：使用 CrossRef 查询**
   ```bash
   python3 fetch_bibtex_crossref.py "论文标题"
   ```

2. **如果失败：尝试使用 DOI**
   - 在论文网站或谷歌学术页面找到 DOI
   ```bash
   python3 fetch_bibtex_crossref.py --doi "10.1109/XXX.XXXX.XXXXXXX"
   ```

3. **仍然失败：使用谷歌学术工具**
   ```bash
   python3 fetch_bibtex.py "论文标题"
   ```

### 已测试的论文示例

以下论文已成功测试（使用 CrossRef）：

```bash
# ORB-SLAM (IEEE TRO 2015)
python3 fetch_bibtex_crossref.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"

# VINS-Mono (IEEE TRO 2018)
python3 fetch_bibtex_crossref.py "VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator"

# DTAM (ICCV 2011)
python3 fetch_bibtex_crossref.py "DTAM: Dense tracking and mapping in real-time"
```

---

## 📖 实用技巧

### 批量查询文献

创建一个文本文件 `papers.txt`，每行一个标题：

```
ORB-SLAM: a Versatile and Accurate Monocular SLAM System
VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator
DTAM: Dense tracking and mapping in real-time
```

然后批量查询：

```bash
while IFS= read -r title; do
  echo "正在查询: $title"
  python3 fetch_bibtex_crossref.py "$title" >> all_refs.bib
  echo "" >> all_refs.bib  # 添加空行分隔
  sleep 2  # 礼貌性延迟
done < papers.txt
```

### 直接添加到项目 ref.bib

```bash
# 从 scripts 目录执行
python3 fetch_bibtex_crossref.py "论文标题" >> ../Biblio/ref.bib
```

### 查找 DOI 的方法

1. **谷歌学术**：搜索论文，点击引用，通常会显示 DOI
2. **论文页面**：IEEE Xplore、ACM DL 等页面上通常显眼位置有 DOI
3. **CrossRef 搜索**：https://search.crossref.org/
4. **DOI.org**：https://www.doi.org/

---

## ⚠️ 常见问题

**Q: CrossRef 找不到某篇论文？**
A: 可能是：
- 论文没有 DOI（如 arXiv 预印本、技术报告）
- 标题拼写不准确
- 使用谷歌学术工具作为备选

**Q: 返回的 BibTeX 格式不符合要求？**
A: CrossRef 返回的格式可能需要微调：
- 检查 citation key（第一个参数）
- 验证作者、年份、页码等关键信息
- 必要时手动编辑

**Q: 提示 "未安装 scholarly 库"？**
A: 运行 `pip3 install scholarly` 安装依赖。

**Q: 谷歌学术查询失败或被封禁？**
A:
- 尝试使用 `--proxy` 选项
- 等待一段时间后重试
- 优先使用 CrossRef 工具

**Q: 如何验证 BibTeX 准确性？**
A:
- 在原始论文网站验证（IEEE Xplore、ACM DL 等）
- 与谷歌学术提供的引用对比
- 检查关键字段：作者、年份、出版社、页码

---

## 📂 项目文件说明

- **`fetch_bibtex_crossref.py`** - CrossRef 查询工具（推荐）
- **`fetch_bibtex.py`** - 谷歌学术查询工具（备选）
- **`requirements.txt`** - Python 依赖列表
- **`README.md`** - 本说明文档

---

## 🔗 相关资源

- **CrossRef API 文档**: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- **Google Scholar**: https://scholar.google.com/
- **DOI.org**: https://www.doi.org/
- **Scholarly 库文档**: https://scholarly.readthedocs.io/

---

## 📝 许可与免责声明

- 本工具仅供学术研究使用
- 请遵守 CrossRef 和 Google Scholar 的使用条款
- 使用前请验证 BibTeX 引用的准确性
- 建议在论文提交前核对所有引用信息

