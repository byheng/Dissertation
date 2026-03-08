# 中文文献 BibTeX 工具使用指南

## 快速开始

### 场景 1: 添加新的中文学位论文

假设你需要引用一篇硕士论文：
- 标题：面向视觉SLAM的低延时位姿优化硬件加速器设计
- 作者：黄坤
- 学校：电子科技大学
- 年份：2025

**步骤：**

```bash
cd /Users/byheng/Dissertation/scripts

# 1. 运行中文文献工具
python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计"

# 2. 按提示输入信息
论文标题 [面向视觉SLAM的低延时位姿优化硬件加速器设计]: [直接回车]
作者（中文全名，多个作者用 ' and ' 分隔）: 黄坤
年份: 2025

文献类型:
  1. 硕士学位论文 (@mastersthesis)
  2. 博士学位论文 (@phdthesis)
  3. 期刊文章 (@article)
  4. 会议论文 (@inproceedings)
选择类型 [1-4]: 1

Citation key (例如: zhang2023slam): huangkun2025vslam
学校: 电子科技大学
地址（城市）: 成都
```

**输出：**

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

**添加到 ref.bib：**

```bash
# 方法1: 直接追加
python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计" >> ../Biblio/ref.bib

# 方法2: 先保存到文件，手动复制
python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计" -o temp.bib
cat temp.bib >> ../Biblio/ref.bib
```

---

### 场景 2: 验证现有的中文文献

**问题：** ref.bib 中已有 6 个中文文献，需要验证是否准确。

**解决方案：** 使用批量验证工具

```bash
cd /Users/byheng/Dissertation/scripts
python3 verify_chinese_refs.py
```

**工具会自动：**
1. 提取 ref.bib 中的所有中文文献
2. 生成每个文献的搜索链接（知网、万方、维普、百度学术）
3. 交互式询问验证结果

**示例输出：**

```
================================================================================
[1/6] 验证文献: huangkun2025vslam
================================================================================

📄 文献信息:
  标题: 面向视觉SLAM的低延时位姿优化硬件加速器设计
  作者: 黄坤
  学校: 电子科技大学
  类型: 硕士学位论文
  地址: 成都
  年份: 2025

🔍 验证链接:
  CNKI: https://kns.cnki.net/kns8/defaultresult/index?kw=...
  万方: https://s.wanfangdata.com.cn/paper?q=...
  维普: http://www.cqvip.com/main/search.aspx?k=...
  百度学术: https://xueshu.baidu.com/s?wd=...

--------------------------------------------------------------------------------
请在上述链接中验证该文献，然后回答以下问题:
--------------------------------------------------------------------------------

1. 是否在数据库中找到该文献? [y/n]: y
2. 在哪个数据库找到? [CNKI/万方/维普/百度学术]: CNKI
3. ref.bib 中的信息是否准确? [y/n]: y

✓ 验证完成

继续验证下一个文献? [y/n]:
```

**验证报告自动保存到：** `chinese_refs_verification.txt`

---

### 场景 3: 添加中文期刊文章

假设要引用期刊综述：
- 标题：视觉SLAM机器人中光束法平差优化芯片研究综述
- 作者：莫霄睿、张惟宜、年成等
- 期刊：集成电路与嵌入式系统
- 卷号：24，期号：11
- 年份：2024

```bash
python3 fetch_bibtex_chinese.py "视觉SLAM机器人中光束法平差优化芯片研究综述"

# 输入信息
作者: 莫霄睿 and 张惟宜 and 年成 and 郭与时 and 牛丽婷 and 张柏雯 and 张春
年份: 2024
文献类型: 3  # 期刊文章
Citation key: mo2024ba_review
期刊名称: 集成电路与嵌入式系统
卷号: 24
期号: 11
页码: [可选，直接回车跳过]
DOI: 10.20193/ices2097-4191.2024.0038
```

**输出：**

```bibtex
@article{mo2024ba_review,
  title={{视觉SLAM机器人中光束法平差优化芯片研究综述}},
  author={莫霄睿 and 张惟宜 and 年成 and 郭与时 and 牛丽婷 and 张柏雯 and 张春},
  journal={集成电路与嵌入式系统},
  volume={24},
  number={11},
  year={2024},
  doi={10.20193/ices2097-4191.2024.0038}
}
```

---

## 常见问题解答

### Q1: 为什么不能像英文文献一样自动查询？

**A:** 中文数据库（知网、万方等）没有公开的 API 接口，无法自动抓取。只能手动验证。

### Q2: 如何确保中文文献信息准确？

**A:** 最佳实践：
1. 在知网或学校图书馆找到原文
2. 复制官方的引用格式
3. 手动转换为 BibTeX 格式
4. 在 ref.bib 前添加验证注释

```bibtex
% 验证来源: 中国知网, 2026-03-06
% 检索 URL: https://kns.cnki.net/...
@mastersthesis{huangkun2025vslam,
  ...
}
```

### Q3: 多作者如何输入？

**A:** 使用 ` and ` 分隔（注意空格）：

```
# 正确
莫霄睿 and 张惟宜 and 年成

# 错误
莫霄睿,张惟宜,年成
莫霄睿、张惟宜、年成
```

### Q4: 标题需要双花括号吗？

**A:** 是的，建议使用双花括号保护中文字符：

```bibtex
title={{面向视觉SLAM的低延时位姿优化硬件加速器设计}}
```

### Q5: Citation key 如何规范命名？

**A:** 建议格式：`作者拼音 + 年份 + 关键词`

```
huangkun2025vslam
mo2024ba_review
zhang2023slam
```

---

## 验证 Checklist

对于每个中文文献，建议验证以下信息：

- [ ] 标题完整且准确
- [ ] 作者姓名正确（注意姓名顺序）
- [ ] 年份准确（学位论文为授予年份，期刊为发表年份）
- [ ] 学校/期刊名称规范
- [ ] 卷号、期号正确（期刊）
- [ ] 学位类型正确（硕士/博士）
- [ ] 地址城市正确
- [ ] Citation key 唯一且规范
- [ ] 添加验证注释

---

## 工具对比

| 文献类型 | 推荐工具 | 说明 |
|---------|---------|------|
| 英文期刊/会议 | `fetch_bibtex_crossref.py` | 自动查询，最快 |
| 英文 arXiv | `fetch_bibtex.py` | 需要 VPN |
| 中文学位论文 | `fetch_bibtex_chinese.py` | 交互式输入 |
| 中文期刊 | `fetch_bibtex_chinese.py` | 交互式输入 |
| 批量验证中文 | `verify_chinese_refs.py` | 生成搜索链接 |

---

## 技巧与建议

1. **优先从官方源获取信息**
   - 学位论文：学校图书馆或知网
   - 期刊文章：期刊官网或知网

2. **保存验证记录**
   ```bibtex
   % 验证: 知网, 2026-03-06, https://kns.cnki.net/xxx
   @mastersthesis{...}
   ```

3. **批量处理**
   - 先收集所有待引用的中文文献列表
   - 集中时间使用工具批量生成
   - 统一验证和添加到 ref.bib

4. **备份重要信息**
   - 保存论文的 URL 或下载 PDF
   - 记录查询时使用的关键词
   - 截图保存验证页面（如需要）

---

## 联系与反馈

如有问题或建议，请：
1. 查看 `README.md` 完整文档
2. 查看 `VERIFICATION_REPORT.md` 了解验证流程
3. 提交 Issue 到项目仓库
