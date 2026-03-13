#!/usr/bin/env python3
"""
批量验证 ref.bib 中所有文献的真实性（通过 CrossRef API）
用法: python3 verify_bib.py [path_to_bib]
"""

import sys
import re
import time
import requests
from difflib import SequenceMatcher

BIB_PATH = "../Biblio/ref.bib"


def parse_bib(path):
    """解析 bib 文件，提取每条文献的 key、title、doi、type"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # 匹配 @type{key, ... }  (支持嵌套花括号)
    pattern = re.compile(r'@(\w+)\{([^,]+),(.+?)(?=\n@|\Z)', re.DOTALL)
    for m in pattern.finditer(content):
        entry_type = m.group(1).lower()
        key = m.group(2).strip()
        body = m.group(3)

        # 跳过注释行开头的
        if key.startswith('%'):
            continue

        # 提取 title（支持嵌套花括号，贪婪到行尾逗号前）
        title_match = re.search(r'title\s*=\s*\{(.+)\}', body)
        title = title_match.group(1).strip() if title_match else ""
        # 清理 LaTeX：先去掉保护花括号，再去掉命令如 \'o
        title = re.sub(r'\{([^{}]*)\}', r'\1', title)  # {EuRoC} -> EuRoC
        title = re.sub(r'\{([^{}]*)\}', r'\1', title)  # 再来一次处理嵌套
        title = re.sub(r"\\['`\"^~=.][a-zA-Z]", lambda m: m.group(0)[-1], title)  # \'o -> o
        title = re.sub(r'\\[a-zA-Z]+\s*', ' ', title)  # \mathrm{} 等 -> 空格
        title = title.replace('$', '').replace('\\', '').replace('  ', ' ').strip()

        # 提取 doi（去掉 LaTeX 转义）
        doi_match = re.search(r'doi\s*=\s*\{(.+?)\}', body)
        doi = doi_match.group(1).strip() if doi_match else ""
        doi = doi.replace('\\_', '_')  # 修复 LaTeX 转义下划线

        # 提取 author
        author_match = re.search(r'author\s*=\s*\{(.+?)\}', body, re.DOTALL)
        author = author_match.group(1).strip() if author_match else ""

        entries.append({
            "key": key,
            "type": entry_type,
            "title": title,
            "doi": doi,
            "author": author,
        })

    return entries


def similarity(a, b):
    """计算两个字符串的相似度 (0~1)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def verify_by_doi(doi):
    """通过 DOI 验证文献是否存在，返回 (存在, 标题)"""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            titles = data.get("message", {}).get("title", [])
            return True, titles[0] if titles else ""
        return False, ""
    except Exception:
        return None, ""  # 网络错误返回 None


def verify_by_title(title):
    """通过标题搜索 CrossRef，返回 (最佳匹配标题, 相似度, DOI)"""
    try:
        url = "https://api.crossref.org/works"
        params = {"query.title": title, "rows": 3,
                  "select": "DOI,title"}
        r = requests.get(url, params=params, timeout=15)
        if r.status_code != 200:
            return None, 0, ""

        items = r.json().get("message", {}).get("items", [])
        if not items:
            return None, 0, ""

        best_title = ""
        best_sim = 0
        best_doi = ""
        for item in items:
            t = item.get("title", [""])[0]
            s = similarity(title, t)
            if s > best_sim:
                best_sim = s
                best_title = t
                best_doi = item.get("DOI", "")

        return best_title, best_sim, best_doi
    except Exception:
        return None, 0, ""


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else BIB_PATH
    entries = parse_bib(path)
    print(f"共解析到 {len(entries)} 条文献\n")

    OK = []       # 验证通过
    SUSPECT = []  # 可疑（标题不匹配或找不到）
    SKIP = []     # 跳过（中文文献等）
    ERROR = []    # 网络错误

    for i, e in enumerate(entries):
        key = e["key"]
        title = e["title"]
        doi = e["doi"]
        tag = f"[{i+1}/{len(entries)}] {key}"

        # 跳过中文文献（CrossRef 对中文覆盖差）
        if re.search(r'[\u4e00-\u9fff]', title):
            print(f"  {tag}: 跳过（中文文献）")
            SKIP.append(e)
            continue

        if not title:
            print(f"  {tag}: 跳过（无标题）")
            SKIP.append(e)
            continue

        # 优先用 DOI 验证
        if doi:
            exists, cr_title = verify_by_doi(doi)
            if exists is None:
                print(f"  {tag}: 网络错误")
                ERROR.append(e)
            elif exists:
                sim = similarity(title, cr_title) if cr_title else 1.0
                if sim >= 0.6:
                    print(f"  {tag}: OK (DOI 验证通过, 相似度 {sim:.2f})")
                    OK.append(e)
                else:
                    print(f"  {tag}: ⚠ DOI 存在但标题不匹配 (相似度 {sim:.2f})")
                    print(f"         本地: {title}")
                    print(f"         远程: {cr_title}")
                    SUSPECT.append({**e, "reason": "DOI存在但标题不匹配",
                                    "remote_title": cr_title, "sim": sim})
            else:
                print(f"  {tag}: ⚠ DOI 不存在: {doi}")
                SUSPECT.append({**e, "reason": "DOI不存在", "remote_title": "", "sim": 0})
            time.sleep(0.3)
            continue

        # 无 DOI，用标题搜索
        cr_title, sim, cr_doi = verify_by_title(title)
        if cr_title is None:
            print(f"  {tag}: 网络错误")
            ERROR.append(e)
        elif sim >= 0.75:
            print(f"  {tag}: OK (标题匹配, 相似度 {sim:.2f})")
            OK.append(e)
        elif sim >= 0.5:
            print(f"  {tag}: ⚠ 标题部分匹配 (相似度 {sim:.2f})")
            print(f"         本地: {title}")
            print(f"         最近: {cr_title}")
            SUSPECT.append({**e, "reason": "标题部分匹配",
                            "remote_title": cr_title, "sim": sim})
        else:
            print(f"  {tag}: ❌ 未找到匹配文献 (最佳相似度 {sim:.2f})")
            print(f"         本地: {title}")
            if cr_title:
                print(f"         最近: {cr_title}")
            SUSPECT.append({**e, "reason": "未找到匹配",
                            "remote_title": cr_title or "", "sim": sim})

        time.sleep(0.3)

    # 汇总
    print("\n" + "=" * 70)
    print(f"验证完成: 通过 {len(OK)}, 可疑 {len(SUSPECT)}, "
          f"跳过 {len(SKIP)}, 网络错误 {len(ERROR)}")
    print("=" * 70)

    if SUSPECT:
        print("\n⚠ 可疑文献清单:")
        print("-" * 70)
        for s in SUSPECT:
            print(f"  Key:    {s['key']}")
            print(f"  标题:   {s['title']}")
            print(f"  原因:   {s['reason']}")
            if s.get("remote_title"):
                print(f"  最近匹配: {s['remote_title']} (相似度: {s['sim']:.2f})")
            print()

    if ERROR:
        print("\n⚠ 网络错误（未能验证）:")
        for e in ERROR:
            print(f"  {e['key']}: {e['title']}")


if __name__ == "__main__":
    main()
