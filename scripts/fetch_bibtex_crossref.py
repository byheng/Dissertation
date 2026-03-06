#!/usr/bin/env python3
"""
CrossRef BibTeX 查询工具（推荐使用，无需反爬虫）
用法: python3 fetch_bibtex_crossref.py "文献标题"
"""

import sys
import argparse
import requests
import json
from typing import Optional


def fetch_bibtex_crossref(title: str, doi: Optional[str] = None) -> Optional[str]:
    """
    从 CrossRef 查询文献的 BibTeX 格式引用

    Args:
        title: 文献标题
        doi: DOI（可选，如果提供则直接查询）

    Returns:
        BibTeX 格式的引用字符串，如果未找到则返回 None
    """
    try:
        # 如果提供了 DOI，直接查询
        if doi:
            print(f"使用 DOI 查询: {doi}")
            bibtex_url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
            headers = {'Accept': 'application/x-bibtex'}
            response = requests.get(bibtex_url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text
            else:
                print(f"DOI 查询失败: HTTP {response.status_code}")
                return None

        # 否则通过标题搜索
        print(f"正在搜索: {title}")
        print("=" * 60)

        # 搜索 CrossRef
        search_url = "https://api.crossref.org/works"
        params = {
            'query.title': title,
            'rows': 1,
            'select': 'DOI,title,author,published-print,container-title,volume,issue,page'
        }

        response = requests.get(search_url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"搜索失败: HTTP {response.status_code}")
            return None

        data = response.json()
        items = data.get('message', {}).get('items', [])

        if not items:
            print("错误：未找到匹配的文献")
            return None

        # 获取第一个结果
        item = items[0]
        found_doi = item.get('DOI')

        if not found_doi:
            print("错误：未找到 DOI")
            return None

        # 显示找到的文献信息
        print("找到文献:")
        print(f"  标题: {item.get('title', ['N/A'])[0]}")

        authors = item.get('author', [])
        if authors:
            author_names = []
            for author in authors[:3]:  # 显示前3个作者
                given = author.get('given', '')
                family = author.get('family', '')
                author_names.append(f"{given} {family}".strip())
            author_str = ', '.join(author_names)
            if len(authors) > 3:
                author_str += ', et al.'
            print(f"  作者: {author_str}")

        pub_date = item.get('published-print', item.get('published-online', {}))
        if pub_date and 'date-parts' in pub_date:
            year = pub_date['date-parts'][0][0]
            print(f"  年份: {year}")

        venue = item.get('container-title', ['N/A'])
        if venue:
            print(f"  来源: {venue[0]}")

        print(f"  DOI: {found_doi}")
        print("=" * 60)

        # 获取 BibTeX
        print("\n正在获取 BibTeX...")
        bibtex_url = f"https://api.crossref.org/works/{found_doi}/transform/application/x-bibtex"
        headers = {'Accept': 'application/x-bibtex'}
        bibtex_response = requests.get(bibtex_url, headers=headers, timeout=10)

        if bibtex_response.status_code == 200:
            return bibtex_response.text
        else:
            print(f"BibTeX 获取失败: HTTP {bibtex_response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print("错误：请求超时，请检查网络连接")
        return None
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求失败 - {str(e)}")
        return None
    except Exception as e:
        print(f"错误：{str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="从 CrossRef 查询文献的 BibTeX 格式引用（推荐使用）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 fetch_bibtex_crossref.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"
  python3 fetch_bibtex_crossref.py --doi "10.1109/TRO.2015.2463671"
  python3 fetch_bibtex_crossref.py -o output.bib "SLAM Survey"

优势:
  - 无需科学上网
  - 无反爬虫限制
  - 速度快且稳定
  - 数据权威（来自出版社）

注意:
  - 仅支持有 DOI 的文献（大多数学术论文都有）
  - 对于会议论文和期刊论文效果最好
        """
    )

    parser.add_argument(
        "title",
        nargs='?',
        help="文献标题"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出到指定文件（可选，默认输出到终端）",
        default=None
    )

    parser.add_argument(
        "--doi",
        help="直接使用 DOI 查询（例如: 10.1109/TRO.2015.2463671）",
        default=None
    )

    args = parser.parse_args()

    # 验证参数
    if not args.title and not args.doi:
        parser.error("必须提供标题或 DOI")

    # 查询 BibTeX
    bibtex = fetch_bibtex_crossref(args.title or "", doi=args.doi)

    if bibtex:
        print("\nBibTeX 引用:")
        print("-" * 60)
        print(bibtex)
        print("-" * 60)

        # 如果指定了输出文件
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(bibtex)
                    f.write('\n')
                print(f"\n已保存到: {args.output}")
            except Exception as e:
                print(f"\n错误：无法保存到文件 - {str(e)}")

        return 0
    else:
        print("\n查询失败。请尝试：")
        print("  1. 检查标题是否正确")
        print("  2. 使用 --doi 参数直接查询（如果知道 DOI）")
        print("  3. 该文献可能没有 DOI（例如：arXiv 预印本）")
        return 1


if __name__ == "__main__":
    sys.exit(main())
