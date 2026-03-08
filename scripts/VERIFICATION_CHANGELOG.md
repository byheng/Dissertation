# 参考文献验证更新日志

## 2026-03-06 更新

### 手动验证的书籍（3 本）

以下书籍已通过出版社官网或 ISBN 手动验证，条目信息准确：

1. **`hartley2003multiple`** - Multiple View Geometry in Computer Vision
   - 作者: Richard Hartley, Andrew Zisserman
   - 出版社: Cambridge University Press
   - 年份: 2003 (第二版)
   - 验证方式: 出版社官网
   - 状态: ✅ 已验证

2. **`warren2013hacker`** - Hacker's Delight
   - 作者: Henry S. Warren
   - 出版社: Pearson Education
   - 年份: 2013 (第二版)
   - 验证方式: 出版社官网/ISBN
   - 状态: ✅ 已验证

3. **`saad2003iterative`** - Iterative Methods for Sparse Linear Systems
   - 作者: Yousef Saad
   - 出版社: SIAM
   - 年份: 2003 (第二版)
   - 验证方式: SIAM 官网
   - 状态: ✅ 已验证

### ref.bib 修改内容

为以上三本书添加了验证注释和完整信息：
- 添加 `% Verified: Manual, 2026-03-06 (Book)` 注释
- 补充 `edition` 字段（第二版）
- 补充 `address` 字段（出版地）
- 统一格式（使用 `=` 对齐）

### 已删除的条目（1 个）

**`seu_fpga_slam`** - 基于FPGA的嵌入式视觉SLAM前端加速器设计与实现
- 作者: 李聪
- 学校: 东南大学
- 删除原因: 知网无法检索到该论文
- 相关引用: 已删除 `Tex/Chap_Intro.tex:144` 中的引用

### 验证工具标记规范

为避免验证工具重复检查已验证的条目，使用以下标记格式：

```bibtex
% Verified: CrossRef, YYYY-MM-DD
@article{key, ...}

% Verified: Manual, YYYY-MM-DD (Book)
@book{key, ...}

% Verified: CNKI, YYYY-MM-DD (Chinese)
@mastersthesis{key, ...}
```

**标记说明：**
- `CrossRef`: 通过 CrossRef API 自动验证
- `Manual`: 手动通过官网或数据库验证
- `CNKI/万方/维普`: 中文文献验证来源
- 日期格式: YYYY-MM-DD

### 下次验证时的跳过规则

验证工具应跳过以下已标记的条目：
1. 包含 `% Verified:` 注释的条目
2. 注释中标记为 `(Book)` 且年份 < 2020 的书籍（书籍版本更新较慢）
3. 注释中标记为 `Manual` 且日期在 6 个月内的条目

---

## 后续待办

### 需要补充完整作者信息的条目

- [ ] `liu2022energy` - author={Liu, Qiang and **others**}
- [ ] `fang2019fpga` - author={Fang, Zhijian and **others**}
- [ ] `li2022fpga` - author={Li, J. and **others**}

### 待验证的中文文献

- [ ] `huangkun2025vslam` - 2025 年论文，可能尚未公开
- [ ] `mo2024ba_review` - 期刊文章，需在知网验证
- [ ] `sjtu_fpga_vio` - 上海交通大学（2020）
- [ ] `nudt_sparse_matrix` - 国防科技大学（2022）
- [ ] `zju_dual_camera` - 浙江大学（2019）

### 建议操作

1. **定期验证（每 6 个月）**：
   - 中文学位论文（检查是否已上传到知网）
   - 最新年份的论文（如 2024-2025 年）

2. **补充信息优先级**：
   - High: 作者信息不完整的条目
   - Medium: 缺少 DOI 的期刊文章
   - Low: 已验证但格式可优化的条目

3. **验证工具改进**：
   - 添加跳过已验证条目的逻辑
   - 生成验证覆盖率报告
   - 支持增量验证（仅验证新增条目）

---

**更新人**: Claude (Haiku 4.5)
**更新日期**: 2026-03-06
