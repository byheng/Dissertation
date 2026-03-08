# BibTeX 文献查询工具

本目录提供完整的 BibTeX 查询工具集，支持**英文文献**和**中文文献**的查询与验证。

---

## 📚 工具概览

| 工具 | 用途 | 适用文献类型 |
|------|------|------------|
| `fetch_bibtex_crossref.py` | CrossRef 查询 | 英文期刊、会议论文（推荐） |
| `fetch_bibtex.py` | Google Scholar 查询 | arXiv、未索引论文（备选） |
| `fetch_bibtex_chinese.py` | 中文文献交互式生成 | 中文学位论文、期刊 |
| `verify_chinese_refs.py` | 批量验证中文文献 | ref.bib 中的中文条目 |

---

## 🌟 推荐工具：CrossRef 查询 (fetch_bibtex_crossref.py)

**优先使用此工具查询英文文献**，具有以下优势：
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

## 🇨🇳 中文文献工具 (fetch_bibtex_chinese.py)

专门用于查询和生成**中文学位论文**、**中文期刊文章**的 BibTeX 条目。

### 为什么需要这个工具？

中文文献（特别是学位论文）通常：
- ❌ 没有 DOI
- ❌ 不在 CrossRef 索引中
- ❌ 谷歌学术可能无法访问或索引不全
- ✅ 主要收录在：中国知网（CNKI）、万方数据、维普网等中文数据库

### 使用方法

**基本用法（交互式生成）：**

```bash
python3 fetch_bibtex_chinese.py "论文标题"
```

**完整示例：生成学位论文 BibTeX**

```bash
python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计"

# 按提示输入信息：
# 作者：黄坤
# 年份：2025
# 类型：1 (硕士学位论文)
# 学校：电子科技大学
# 地址：成都
# Citation key: huangkun2025vslam
```

**输出示例：**

```bibtex
@mastersthesis{huangkun2025vslam,
  title={{面向视觉SLAM的低延时位姿优化硬件加速器设计}},
  author={黄坤},
  school={电子科技大学},
  year={2025},
  type={硕士学位论文},
  address={成都}
}
```

**保存到文件：**

```bash
python3 fetch_bibtex_chinese.py "论文标题" -o output.bib
```

**验证模式（检查文献是否存在）：**

```bash
python3 fetch_bibtex_chinese.py --verify "论文标题" --author "作者" --year "2025" --school "大学名"
```

### 支持的文献类型

1. **硕士学位论文** (`@mastersthesis`)
   - 需要：标题、作者、学校、年份、地址

2. **博士学位论文** (`@phdthesis`)
   - 需要：标题、作者、学校、年份、地址

3. **期刊文章** (`@article`)
   - 需要：标题、作者、期刊名、卷号、期号、年份
   - 可选：DOI

4. **会议论文** (`@inproceedings`)
   - 需要：标题、作者、会议名、年份
   - 可选：页码、地点

### 中文数据库验证

工具会提示你在以下数据库中手动验证文献：

- **中国知网 (CNKI)**: https://www.cnki.net/
- **万方数据**: http://www.wanfangdata.com.cn/
- **维普网**: http://www.cqvip.com/
- **百度学术**: https://xueshu.baidu.com/

### 批量验证 ref.bib 中的中文文献

使用专用工具批量验证：

```bash
python3 verify_chinese_refs.py
```

**功能：**
- 自动提取 ref.bib 中的 6 个中文文献
- 生成每个文献的知网、万方等搜索链接
- 交互式验证每个文献
- 生成验证报告

**验证的中文文献：**
1. `huangkun2025vslam` - 黄坤硕士论文（电子科技大学, 2025）
2. `mo2024ba_review` - 莫霄睿综述（集成电路与嵌入式系统, 2024）
3. `seu_fpga_slam` - 李聪硕士论文（东南大学, 2021）
4. `sjtu_fpga_vio` - 王晓东硕士论文（上海交通大学, 2020）
5. `nudt_sparse_matrix` - 张明博士论文（国防科技大学, 2022）
6. `zju_dual_camera` - 赵宏伟硕士论文（浙江大学, 2019）

### 注意事项

1. **手动验证必不可少**：
   - 中文数据库通常没有 API 接口
   - 需要在浏览器中手动搜索验证
   - 工具提供直接搜索链接，简化流程

2. **Citation key 规范**：
   - 格式：`作者拼音 + 年份 + 关键词`
   - 示例：`zhang2023slam`, `huangkun2025vslam`

3. **中文字符处理**：
   - 标题使用双花括号：`{{标题}}`
   - 作者使用中文全名
   - 多作者用 ` and ` 分隔

4. **验证建议**：
   - 优先在学校官网或知网查询学位论文
   - 记录验证来源和时间
   - 添加验证注释到 BibTeX 条目

---

## 🚀 快速开始指南

### 推荐工作流程

**对于英文文献：**

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

**对于中文文献：**

1. **使用中文文献工具**
   ```bash
   python3 fetch_bibtex_chinese.py "论文标题"
   ```

2. **在提示的数据库中验证**
   - 打开提供的知网、万方等链接
   - 复制准确的信息

3. **批量验证已有条目**
   ```bash
   python3 verify_chinese_refs.py
   ```

### 已测试的论文示例

**英文文献**（使用 CrossRef）：

```bash
# ORB-SLAM (IEEE TRO 2015)
python3 fetch_bibtex_crossref.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"

# VINS-Mono (IEEE TRO 2018)
python3 fetch_bibtex_crossref.py "VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator"

# DTAM (ICCV 2011)
python3 fetch_bibtex_crossref.py "DTAM: Dense tracking and mapping in real-time"
```

**中文文献**（使用中文工具）：

```bash
# 学位论文示例
python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计"
# 输入：作者=黄坤, 学校=电子科技大学, 年份=2025

# 期刊文章示例
python3 fetch_bibtex_chinese.py "视觉SLAM机器人中光束法平差优化芯片研究综述"
# 输入：作者=莫霄睿 and 张惟宜 and ..., 期刊=集成电路与嵌入式系统, 年份=2024

# 批量验证
python3 verify_chinese_refs.py
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

**Q: 如何查询中文文献？**
A:
- 使用 `fetch_bibtex_chinese.py` 交互式生成
- 手动在知网、万方等数据库验证信息
- 中文文献通常没有 DOI，需要手动输入

**Q: 中文文献无法在 CrossRef 或 Google Scholar 找到？**
A: 这是正常的，因为：
- 中文学位论文通常只收录在知网、万方等中文数据库
- 这些数据库没有公开 API
- 使用 `fetch_bibtex_chinese.py` 或 `verify_chinese_refs.py` 工具
- 工具会提供直接的搜索链接

**Q: 如何批量验证 ref.bib 中的中文文献？**
A:
```bash
python3 verify_chinese_refs.py
```
工具会自动提取所有中文文献并生成验证链接

**Q: 中文作者姓名如何输入？**
A:
- 使用中文全名：`张三` 而非 `Zhang, San`
- 多作者用 ` and ` 分隔：`张三 and 李四 and 王五`
- 保持与原文一致

**Q: 学位论文的 type 字段如何填写？**
A:
- 硕士论文：`type={硕士学位论文}`
- 博士论文：`type={博士学位论文}` 或省略（默认）
- 保持中文以符合中文文献引用规范

---

## 📂 项目文件说明

**英文文献查询工具：**
- **`fetch_bibtex_crossref.py`** - CrossRef 查询工具（推荐，用于英文期刊/会议论文）
- **`fetch_bibtex.py`** - 谷歌学术查询工具（备选，用于 arXiv 等）

**中文文献查询工具：**
- **`fetch_bibtex_chinese.py`** - 中文文献交互式生成工具
- **`verify_chinese_refs.py`** - 批量验证 ref.bib 中的中文文献

**验证报告：**
- **`VERIFICATION_REPORT.md`** - 文献验证详细报告
- **`chinese_refs_verification.txt`** - 中文文献验证报告（运行后生成）

**其他文件：**
- **`requirements.txt`** - Python 依赖列表
- **`README.md`** - 本说明文档

---

## 🔗 相关资源

**英文文献数据库：**
- **CrossRef API 文档**: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- **Google Scholar**: https://scholar.google.com/
- **DOI.org**: https://www.doi.org/
- **Scholarly 库文档**: https://scholarly.readthedocs.io/

**中文文献数据库：**
- **中国知网 (CNKI)**: https://www.cnki.net/
- **万方数据**: http://www.wanfangdata.com.cn/
- **维普网**: http://www.cqvip.com/
- **百度学术**: https://xueshu.baidu.com/

---

## 📝 许可与免责声明

- 本工具仅供学术研究使用
- 请遵守 CrossRef 和 Google Scholar 的使用条款
- 使用前请验证 BibTeX 引用的准确性
- 建议在论文提交前核对所有引用信息

