#!/usr/bin/env python3
"""
中文文献 BibTeX 查询工具
支持：百度学术、Google Scholar（中文索引）
用法: python3 fetch_bibtex_chinese.py "论文标题"
"""

import sys
import argparse
import requests
import time
from typing import Optional, Dict
from urllib.parse import quote
import re


def search_baidu_scholar(title: str) -> Optional[Dict]:
    """
    通过百度学术搜索中文文献信息

    Args:
        title: 文献标题

    Returns:
        包含文献信息的字典
    """
    try:
        print(f"正在百度学术搜索: {title}")
        print("=" * 60)

        # 构建百度学术搜索 URL
        search_url = f"https://xueshu.baidu.com/s?wd={quote(title)}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        response = requests.get(search_url, headers=headers, timeout=10)

        if response.status_code == 200:
            # 简单解析（实际需要更复杂的 HTML 解析）
            content = response.text

            # 尝试提取基本信息
            # 注意：百度学术的 HTML 结构可能变化，这里只是示例
            info = {
                'title': title,
                'url': search_url,
                'found': '学位论文' in content or '期刊' in content,
                'source': 'baidu_scholar'
            }

            return info
        else:
            print(f"搜索失败: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"百度学术搜索出错: {str(e)}")
        return None


def search_google_scholar_chinese(title: str) -> Optional[Dict]:
    """
    通过 Google Scholar 搜索中文文献（需要访问 Google）
    """
    try:
        from scholarly import scholarly

        print(f"正在 Google Scholar 搜索: {title}")
        print("=" * 60)

        search_query = scholarly.search_pubs(title)
        paper = next(search_query, None)

        if paper:
            bib = paper.get('bib', {})
            return {
                'title': bib.get('title', title),
                'author': ', '.join(bib.get('author', [])),
                'year': bib.get('pub_year', 'N/A'),
                'venue': bib.get('venue', 'N/A'),
                'found': True,
                'source': 'google_scholar'
            }
        else:
            return None

    except ImportError:
        print("提示：未安装 scholarly 库，跳过 Google Scholar 搜索")
        return None
    except Exception as e:
        print(f"Google Scholar 搜索出错: {str(e)}")
        return None


def generate_chinese_bibtex(info: Dict) -> str:
    """
    根据用户输入生成中文文献的 BibTeX 条目
    """
    print("\n请提供以下信息以生成 BibTeX 条目:")
    print("-" * 60)

    # 获取基本信息
    title = input(f"论文标题 [{info.get('title', '')}]: ").strip() or info.get('title', '')
    author = input("作者（中文全名，多个作者用 ' and ' 分隔）: ").strip()
    year = input("年份: ").strip()

    # 判断文献类型
    print("\n文献类型:")
    print("  1. 硕士学位论文 (@mastersthesis)")
    print("  2. 博士学位论文 (@phdthesis)")
    print("  3. 期刊文章 (@article)")
    print("  4. 会议论文 (@inproceedings)")
    doc_type = input("选择类型 [1-4]: ").strip()

    # 根据类型生成 BibTeX
    citation_key = input("Citation key (例如: zhang2023slam): ").strip()

    if doc_type == '1':
        # 硕士学位论文
        school = input("学校: ").strip()
        address = input("地址（城市）: ").strip()

        bibtex = f"""@mastersthesis{{{citation_key},
  title={{{{{title}}}}}},
  author={{{author}}},
  school={{{school}}},
  year={{{year}}},
  type={{硕士学位论文}},
  address={{{address}}}
}}"""

    elif doc_type == '2':
        # 博士学位论文
        school = input("学校: ").strip()
        address = input("地址（城市）: ").strip()

        bibtex = f"""@phdthesis{{{citation_key},
  title={{{{{title}}}}}},
  author={{{author}}},
  school={{{school}}},
  year={{{year}}},
  address={{{address}}}
}}"""

    elif doc_type == '3':
        # 期刊文章
        journal = input("期刊名称: ").strip()
        volume = input("卷号 (可选): ").strip()
        number = input("期号 (可选): ").strip()
        pages = input("页码 (可选): ").strip()
        doi = input("DOI (可选): ").strip()

        bibtex = f"""@article{{{citation_key},
  title={{{{{title}}}}}},
  author={{{author}}},
  journal={{{journal}}},"""

        if volume:
            bibtex += f"\n  volume={{{volume}}},"
        if number:
            bibtex += f"\n  number={{{number}}},"
        if pages:
            bibtex += f"\n  pages={{{pages}}},"
        bibtex += f"\n  year={{{year}}},"
        if doi:
            bibtex += f"\n  doi={{{doi}}}"

        bibtex += "\n}"

    elif doc_type == '4':
        # 会议论文
        booktitle = input("会议名称: ").strip()
        pages = input("页码 (可选): ").strip()
        address = input("会议地点 (可选): ").strip()

        bibtex = f"""@inproceedings{{{citation_key},
  title={{{{{title}}}}}},
  author={{{author}}},
  booktitle={{{booktitle}}},"""

        if pages:
            bibtex += f"\n  pages={{{pages}}},"
        bibtex += f"\n  year={{{year}}},"
        if address:
            bibtex += f"\n  address={{{address}}}"

        bibtex += "\n}"

    else:
        print("无效的类型选择")
        return None

    return bibtex


def verify_chinese_paper(title: str, author: str = "", year: str = "",
                        school: str = "", journal: str = "") -> Dict:
    """
    交互式验证中文论文信息
    返回验证结果供用户确认
    """
    print(f"\n正在验证中文文献: {title}")
    print("=" * 60)

    # 提示用户手动验证
    print("\n请在以下数据库中手动验证该文献:")
    print("  1. 中国知网 (CNKI): https://www.cnki.net/")
    print("  2. 万方数据: http://www.wanfangdata.com.cn/")
    print("  3. 维普网: http://www.cqvip.com/")
    print("  4. 百度学术: https://xueshu.baidu.com/")

    if school:
        print(f"\n  搜索关键词: {title} {author} {school}")
    elif journal:
        print(f"\n  搜索关键词: {title} {author} {journal}")
    else:
        print(f"\n  搜索关键词: {title} {author}")

    verified = input("\n是否已在上述数据库中找到该文献? [y/n]: ").strip().lower()

    result = {
        'title': title,
        'verified': verified == 'y',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    if verified == 'y':
        data_source = input("在哪个数据库找到的? [CNKI/万方/维普/百度学术]: ").strip()
        result['source'] = data_source

        url = input("文献 URL (可选): ").strip()
        if url:
            result['url'] = url

        print("\n✓ 验证完成")
    else:
        print("\n✗ 未找到，请检查文献信息是否准确")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="中文文献 BibTeX 查询与生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式生成 BibTeX
  python3 fetch_bibtex_chinese.py "面向视觉SLAM的低延时位姿优化硬件加速器设计"

  # 验证已有条目
  python3 fetch_bibtex_chinese.py --verify "黄坤" "2025" "电子科技大学"

  # 从知网导出的 BibTeX 文件转换
  python3 fetch_bibtex_chinese.py --convert input.bib -o output.bib

支持的中文数据库:
  - 中国知网 (CNKI)
  - 万方数据
  - 维普网
  - 百度学术

注意事项:
  1. 中文文献通常没有 DOI
  2. 学位论文需要使用 @mastersthesis 或 @phdthesis
  3. 作者姓名使用中文全名
  4. 建议在 BibTeX 条目前添加验证注释
        """
    )

    parser.add_argument(
        "title",
        nargs='?',
        help="论文标题"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出到指定文件",
        default=None
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="验证模式：检查文献是否存在于中文数据库"
    )

    parser.add_argument(
        "--author",
        help="作者姓名（用于验证）",
        default=""
    )

    parser.add_argument(
        "--year",
        help="年份（用于验证）",
        default=""
    )

    parser.add_argument(
        "--school",
        help="学校（学位论文）",
        default=""
    )

    parser.add_argument(
        "--journal",
        help="期刊名称",
        default=""
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="自动模式（尝试百度学术搜索）"
    )

    args = parser.parse_args()

    if not args.title:
        parser.print_help()
        return 1

    # 验证模式
    if args.verify:
        result = verify_chinese_paper(
            args.title,
            author=args.author,
            year=args.year,
            school=args.school,
            journal=args.journal
        )

        print("\n验证结果:")
        print("-" * 60)
        for key, value in result.items():
            print(f"  {key}: {value}")

        return 0 if result['verified'] else 1

    # 自动搜索模式
    if args.auto:
        # 尝试百度学术
        info = search_baidu_scholar(args.title)

        # 如果失败，尝试 Google Scholar
        if not info or not info.get('found'):
            info = search_google_scholar_chinese(args.title)

        if info and info.get('found'):
            print("\n找到文献信息:")
            print("-" * 60)
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print("\n未找到文献，切换到交互式输入模式...")
            info = {'title': args.title}
    else:
        info = {'title': args.title}

    # 交互式生成 BibTeX
    bibtex = generate_chinese_bibtex(info)

    if bibtex:
        print("\n生成的 BibTeX 条目:")
        print("=" * 60)
        print(bibtex)
        print("=" * 60)

        # 保存到文件
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write("% 验证来源: 手动输入\n")
                    f.write(f"% 验证时间: {time.strftime('%Y-%m-%d')}\n")
                    f.write(bibtex)
                    f.write('\n')
                print(f"\n已保存到: {args.output}")
            except Exception as e:
                print(f"\n错误：无法保存到文件 - {str(e)}")

        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
