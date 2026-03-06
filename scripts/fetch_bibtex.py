#!/usr/bin/env python3
"""
谷歌学术 BibTeX 查询工具
用法: python fetch_bibtex.py "文献标题"
"""

import sys
import argparse
import time
from typing import Optional

try:
    from scholarly import scholarly, ProxyGenerator
except ImportError:
    print("错误：未安装 scholarly 库")
    print("请运行: pip3 install scholarly")
    sys.exit(1)


def fetch_bibtex(title: str, use_proxy: bool = False, use_selenium: bool = False, retry: int = 3) -> Optional[str]:
    """
    从谷歌学术查询文献的 BibTeX 格式引用

    Args:
        title: 文献标题
        use_proxy: 是否使用代理（可选，用于规避反爬虫）
        use_selenium: 是否使用 Selenium（需要 Chrome 浏览器）
        retry: 重试次数

    Returns:
        BibTeX 格式的引用字符串，如果未找到则返回 None
    """
    for attempt in range(retry):
        try:
            if attempt > 0:
                wait_time = 5 * (attempt + 1)
                print(f"\n第 {attempt + 1} 次重试，等待 {wait_time} 秒...")
                time.sleep(wait_time)

            # 配置 scholarly
            if use_selenium:
                try:
                    from selenium import webdriver
                    from scholarly import ProxyGenerator

                    print("使用 Selenium 模式（需要 Chrome 浏览器）...")
                    pg = ProxyGenerator()
                    pg.Selenium()
                    scholarly.use_proxy(pg)
                except Exception as e:
                    print(f"Selenium 初始化失败: {e}")
                    print("尝试使用免费代理...")
                    use_proxy = True

            if use_proxy and not use_selenium:
                print("使用免费代理模式...")
                try:
                    pg = ProxyGenerator()
                    pg.FreeProxies()
                    scholarly.use_proxy(pg)
                except Exception as e:
                    print(f"代理初始化失败: {e}")

            print(f"正在搜索: {title}")
            print("=" * 60)

            # 搜索文献
            search_query = scholarly.search_pubs(title)

            # 获取第一个结果
            paper = next(search_query, None)

            if paper is None:
                print("错误：未找到匹配的文献")
                if attempt < retry - 1:
                    continue
                return None

            # 显示找到的文献信息
            print(f"找到文献:")
            print(f"  标题: {paper.get('bib', {}).get('title', 'N/A')}")
            print(f"  作者: {', '.join(paper.get('bib', {}).get('author', ['N/A']))}")
            print(f"  年份: {paper.get('bib', {}).get('pub_year', 'N/A')}")
            print(f"  来源: {paper.get('bib', {}).get('venue', 'N/A')}")
            print("=" * 60)

            # 获取 BibTeX
            bibtex = scholarly.bibtex(paper)

            return bibtex

        except StopIteration:
            print("错误：未找到匹配的文献")
            return None
        except Exception as e:
            error_msg = str(e)
            print(f"错误：{error_msg}")

            # 如果是反爬虫错误
            if "Cannot Fetch" in error_msg or "blocked" in error_msg.lower():
                print("\n遇到谷歌学术反爬虫限制。")
                if not use_proxy and not use_selenium:
                    print("建议：")
                    print("  1. 使用 --proxy 参数启用代理")
                    print("  2. 使用 --selenium 参数启用 Selenium 模式（需要 Chrome）")
                    print("  3. 稍后重试")

                if attempt < retry - 1:
                    continue

            return None

    return None


def main():
    parser = argparse.ArgumentParser(
        description="从谷歌学术查询文献的 BibTeX 格式引用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 fetch_bibtex.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"
  python3 fetch_bibtex.py --proxy "Visual SLAM: a Survey"
  python3 fetch_bibtex.py --selenium "SLAM Survey"
  python3 fetch_bibtex.py -o output.bib "SLAM Survey"
        """
    )

    parser.add_argument(
        "title",
        help="文献标题"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出到指定文件（可选，默认输出到终端）",
        default=None
    )

    parser.add_argument(
        "--proxy",
        action="store_true",
        help="使用免费代理（用于规避反爬虫限制）"
    )

    parser.add_argument(
        "--selenium",
        action="store_true",
        help="使用 Selenium 模式（需要安装 Chrome 浏览器）"
    )

    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="重试次数（默认: 3）"
    )

    args = parser.parse_args()

    # 查询 BibTeX
    bibtex = fetch_bibtex(
        args.title,
        use_proxy=args.proxy,
        use_selenium=args.selenium,
        retry=args.retry
    )

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
        print("\n查询失败。请检查：")
        print("  1. 网络连接是否正常")
        print("  2. 是否能访问谷歌学术（国内用户可能需要科学上网）")
        print("  3. 尝试使用 --proxy 或 --selenium 参数")
        return 1


if __name__ == "__main__":
    sys.exit(main())
