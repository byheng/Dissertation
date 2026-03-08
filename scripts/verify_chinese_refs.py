#!/usr/bin/env python3
"""
批量验证 ref.bib 中的中文文献
提供知网、万方等数据库的直接搜索链接
"""

import sys
import re
from urllib.parse import quote
from typing import List, Dict


# ref.bib 中的中文文献列表
CHINESE_REFS = [
    {
        'key': 'huangkun2025vslam',
        'title': '面向视觉SLAM的低延时位姿优化硬件加速器设计',
        'author': '黄坤',
        'school': '电子科技大学',
        'year': '2025',
        'type': '硕士学位论文',
        'address': '成都'
    },
    {
        'key': 'mo2024ba_review',
        'title': '视觉SLAM机器人中光束法平差优化芯片研究综述',
        'author': '莫霄睿 and 张惟宜 and 年成 and 郭与时 and 牛丽婷 and 张柏雯 and 张春',
        'journal': '集成电路与嵌入式系统',
        'volume': '24',
        'number': '11',
        'year': '2024',
        'doi': '10.20193/ices2097-4191.2024.0038'
    },
    {
        'key': 'seu_fpga_slam',
        'author': '李聪',
        'title': '基于FPGA的嵌入式视觉SLAM前端加速器设计与实现',
        'school': '东南大学',
        'year': '2021',
        'address': '南京'
    },
    {
        'key': 'sjtu_fpga_vio',
        'author': '王晓东',
        'title': '基于FPGA的视觉惯性里程计硬件加速技术研究',
        'school': '上海交通大学',
        'year': '2020',
        'address': '上海'
    },
    {
        'key': 'nudt_sparse_matrix',
        'author': '张明',
        'title': '面向移动机器人的高性能视觉导航硬件架构研究',
        'school': '国防科技大学',
        'year': '2022',
        'address': '长沙'
    },
    {
        'key': 'zju_dual_camera',
        'author': '赵宏伟',
        'title': '基于SoC平台的实时双目视觉里程计系统研究',
        'school': '浙江大学',
        'year': '2019',
        'address': '杭州'
    }
]


def generate_search_urls(ref: Dict) -> Dict[str, str]:
    """生成各个数据库的搜索链接"""
    title = ref.get('title', '')
    author = ref.get('author', '').split(' and ')[0]  # 取第一作者
    school = ref.get('school', '')
    year = ref.get('year', '')

    # 构建搜索关键词
    keywords = f"{title} {author}"
    if school:
        keywords += f" {school}"

    urls = {
        'CNKI': f"https://kns.cnki.net/kns8/defaultresult/index?kw={quote(keywords)}&korder=SU",
        '万方': f"https://s.wanfangdata.com.cn/paper?q={quote(keywords)}",
        '维普': f"http://www.cqvip.com/main/search.aspx?k={quote(keywords)}",
        '百度学术': f"https://xueshu.baidu.com/s?wd={quote(keywords)}"
    }

    return urls


def print_ref_info(ref: Dict, index: int, total: int):
    """打印文献信息和验证链接"""
    print("\n" + "=" * 80)
    print(f"[{index}/{total}] 验证文献: {ref['key']}")
    print("=" * 80)

    print(f"\n📄 文献信息:")
    print(f"  标题: {ref.get('title', 'N/A')}")
    print(f"  作者: {ref.get('author', 'N/A')}")

    if 'school' in ref:
        print(f"  学校: {ref['school']}")
        print(f"  类型: {ref.get('type', '学位论文')}")
        print(f"  地址: {ref.get('address', 'N/A')}")
    elif 'journal' in ref:
        print(f"  期刊: {ref['journal']}")
        print(f"  卷号: {ref.get('volume', 'N/A')}")
        print(f"  期号: {ref.get('number', 'N/A')}")
        if 'doi' in ref:
            print(f"  DOI: {ref['doi']}")

    print(f"  年份: {ref['year']}")

    print(f"\n🔍 验证链接:")
    urls = generate_search_urls(ref)
    for name, url in urls.items():
        print(f"  {name}: {url}")


def verify_ref_interactive(ref: Dict) -> Dict:
    """交互式验证单个文献"""
    result = {
        'key': ref['key'],
        'verified': False,
        'issues': [],
        'notes': ''
    }

    print("\n" + "-" * 80)
    print("请在上述链接中验证该文献，然后回答以下问题:")
    print("-" * 80)

    # 询问是否找到
    found = input("\n1. 是否在数据库中找到该文献? [y/n]: ").strip().lower()

    if found == 'y':
        result['verified'] = True

        # 询问在哪个数据库找到
        source = input("2. 在哪个数据库找到? [CNKI/万方/维普/百度学术]: ").strip()
        result['source'] = source

        # 询问信息是否准确
        accurate = input("3. ref.bib 中的信息是否准确? [y/n]: ").strip().lower()

        if accurate != 'y':
            print("\n请描述发现的问题:")
            print("  a. 标题错误")
            print("  b. 作者错误")
            print("  c. 年份错误")
            print("  d. 学校/期刊错误")
            print("  e. 其他")

            issues = input("选择选项 (可多选，用逗号分隔): ").strip()
            if issues:
                result['issues'] = [x.strip() for x in issues.split(',')]

            notes = input("详细说明 (可选): ").strip()
            if notes:
                result['notes'] = notes

        print("\n✓ 验证完成")
    else:
        print("\n✗ 未找到该文献")
        reason = input("可能的原因 (可选): ").strip()
        if reason:
            result['notes'] = reason

    return result


def batch_verify():
    """批量验证所有中文文献"""
    print("=" * 80)
    print("中文文献批量验证工具")
    print("=" * 80)
    print(f"\n共有 {len(CHINESE_REFS)} 个中文文献需要验证")
    print("\n提示:")
    print("  - 请在浏览器中打开提供的链接")
    print("  - 验证文献的标题、作者、年份等信息")
    print("  - 按 Enter 继续，Ctrl+C 退出")

    input("\n按 Enter 开始验证...")

    results = []

    for i, ref in enumerate(CHINESE_REFS, 1):
        print_ref_info(ref, i, len(CHINESE_REFS))

        result = verify_ref_interactive(ref)
        results.append(result)

        if i < len(CHINESE_REFS):
            cont = input("\n继续验证下一个文献? [y/n]: ").strip().lower()
            if cont != 'y':
                print("\n验证已中断")
                break

    # 生成验证报告
    print("\n" + "=" * 80)
    print("验证报告")
    print("=" * 80)

    verified_count = sum(1 for r in results if r['verified'])
    print(f"\n总计: {len(results)} 个文献")
    print(f"已验证: {verified_count} 个")
    print(f"未找到: {len(results) - verified_count} 个")

    # 详细报告
    print("\n详细结果:")
    print("-" * 80)

    for result in results:
        status = "✓" if result['verified'] else "✗"
        print(f"\n{status} {result['key']}")

        if result['verified']:
            print(f"  来源: {result.get('source', 'N/A')}")

            if result['issues']:
                print(f"  问题: {', '.join(result['issues'])}")

            if result['notes']:
                print(f"  备注: {result['notes']}")
        else:
            if result['notes']:
                print(f"  原因: {result['notes']}")

    # 保存报告
    with open('chinese_refs_verification.txt', 'w', encoding='utf-8') as f:
        f.write("中文文献验证报告\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"验证时间: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总计: {len(results)} 个文献\n")
        f.write(f"已验证: {verified_count} 个\n")
        f.write(f"未找到: {len(results) - verified_count} 个\n\n")

        for result in results:
            f.write("-" * 80 + "\n")
            f.write(f"Citation Key: {result['key']}\n")
            f.write(f"状态: {'已验证' if result['verified'] else '未找到'}\n")

            if result.get('source'):
                f.write(f"来源: {result['source']}\n")

            if result.get('issues'):
                f.write(f"问题: {', '.join(result['issues'])}\n")

            if result.get('notes'):
                f.write(f"备注: {result['notes']}\n")

            f.write("\n")

    print(f"\n报告已保存到: chinese_refs_verification.txt")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("用法: python3 verify_chinese_refs.py")
        print("\n功能:")
        print("  批量验证 ref.bib 中的中文文献")
        print("  自动生成知网、万方等数据库的搜索链接")
        print("  交互式收集验证结果")
        print("  生成验证报告")
        return 0

    try:
        batch_verify()
        return 0
    except KeyboardInterrupt:
        print("\n\n验证已中断")
        return 1
    except Exception as e:
        print(f"\n错误: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
