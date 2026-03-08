#!/usr/bin/env python3
"""批量验证 ref.bib 中的文献条目"""

import subprocess
import time
import re

# 从 ref.bib 提取的主要论文标题（排除中文论文和书籍）
papers_to_verify = [
    ("qin2018vins", "VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator"),
    ("forster2014svo", "SVO: Fast Semi-Direct Monocular Visual Odometry"),
    ("mourikis2007multi", "A multi-state constraint Kalman filter for vision-aided inertial navigation"),
    ("mur2015orb", "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"),
    ("leutenegger2015keyframe", "Keyframe-based visual-inertial odometry using nonlinear optimization"),
    ("engel2014lsd", "LSD-SLAM: Large-Scale Direct Monocular SLAM"),
    ("bloesch2015robust", "Robust Visual Inertial Odometry Using a Direct EKF-Based Method"),
    ("mur2017orb", "Orb-slam2: An open-source slam system for monocular, stereo, and rgb-d cameras"),
    ("campos2021orb", "ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial, and Multimap SLAM"),
    ("fan2024schurvins", "SchurVINS: Schur Complement-Based Lightweight Visual Inertial Navigation System"),
    ("triggs1999bundle", "Bundle adjustment—a modern synthesis"),
    ("Burri25012016", "The EuRoC Micro Aerial Vehicle Datasets"),
    ("schubert2018vidataset", "The TUM VI Benchmark for Evaluating Visual-Inertial Odometry"),
    ("guo2022fpga", "An FPGA-Based Accelerator for Local Bundle Adjustment of Stereo Visual Odometry"),
    ("forster2016svo", "SVO: Semi-Direct Visual Odometry for Monocular and Multicamera Systems"),
    ("forster2016onmanifold", "On-Manifold Preintegration for Real-Time Visual-Inertial Odometry"),
    ("bailey2006simultaneous", "Simultaneous localization and mapping (SLAM): Part II"),
    ("kummerle2011g", "g 2 o: A general framework for graph optimization"),
    ("cadena2017past", "Past, present, and future of simultaneous localization and mapping"),
    ("davison2007monoslam", "MonoSLAM: Real-time single camera SLAM"),
    ("newcombe2011dtam", "DTAM: Dense tracking and mapping in real-time"),
    ("teed2020raft", "RAFT: Recurrent all-pairs field transforms for optical flow"),
    ("liu2019eslam", "eSLAM: An energy-efficient accelerator for real-time ORB-SLAM on FPGA platform"),
    ("suleiman2019navion", "Navion: A fully integrated energy-efficient visual-inertial odometry accelerator"),
    ("rosten2006machine", "Machine learning for high-speed corner detection"),
    ("lowe2004distinctive", "Distinctive image features from scale-invariant keypoints"),
    ("rublee2011orb", "ORB: An efficient alternative to SIFT or SURF"),
    ("fischler1981random", "Random sample consensus"),
    ("klein2007parallel", "Parallel tracking and mapping for small AR workspaces"),
    ("engel2017direct", "Direct sparse odometry"),
    ("durrant2002uncertain", "Uncertain geometry in robotics"),
]

results = []

print("开始批量验证文献条目...")
print("=" * 80)

for citation_key, title in papers_to_verify:
    print(f"\n验证: {citation_key}")
    print(f"标题: {title}")
    print("-" * 80)

    try:
        cmd = ["python3", "fetch_bibtex_crossref.py", title]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

        # 提取年份和DOI
        year_match = re.search(r'年份: (\d{4})', result.stdout)
        doi_match = re.search(r'DOI: ([\d.\/\w-]+)', result.stdout)

        if "找到文献" in result.stdout:
            year = year_match.group(1) if year_match else "Unknown"
            doi = doi_match.group(1) if doi_match else "Unknown"

            results.append({
                'key': citation_key,
                'title': title,
                'status': 'Found',
                'year': year,
                'doi': doi
            })
            print(f"✓ 找到: Year={year}, DOI={doi}")
        else:
            results.append({
                'key': citation_key,
                'title': title,
                'status': 'Not Found',
                'year': 'N/A',
                'doi': 'N/A'
            })
            print(f"✗ 未找到")

    except subprocess.TimeoutExpired:
        results.append({
            'key': citation_key,
            'title': title,
            'status': 'Timeout',
            'year': 'N/A',
            'doi': 'N/A'
        })
        print(f"✗ 超时")
    except Exception as e:
        results.append({
            'key': citation_key,
            'title': title,
            'status': f'Error: {str(e)}',
            'year': 'N/A',
            'doi': 'N/A'
        })
        print(f"✗ 错误: {e}")

    # 延迟避免频繁请求
    time.sleep(2)

# 生成报告
print("\n" + "=" * 80)
print("验证报告摘要")
print("=" * 80)

found = [r for r in results if r['status'] == 'Found']
not_found = [r for r in results if r['status'] == 'Not Found']
errors = [r for r in results if r['status'] not in ['Found', 'Not Found']]

print(f"\n总计: {len(results)} 条")
print(f"找到: {len(found)} 条")
print(f"未找到: {len(not_found)} 条")
print(f"错误/超时: {len(errors)} 条")

if not_found:
    print("\n未找到的条目:")
    for r in not_found:
        print(f"  - {r['key']}: {r['title']}")

if errors:
    print("\n出错的条目:")
    for r in errors:
        print(f"  - {r['key']}: {r['status']}")

# 保存详细报告
with open('verification_report.txt', 'w', encoding='utf-8') as f:
    f.write("文献验证详细报告\n")
    f.write("=" * 80 + "\n\n")
    for r in results:
        f.write(f"Citation Key: {r['key']}\n")
        f.write(f"Title: {r['title']}\n")
        f.write(f"Status: {r['status']}\n")
        f.write(f"Year: {r['year']}\n")
        f.write(f"DOI: {r['doi']}\n")
        f.write("-" * 80 + "\n\n")

print("\n详细报告已保存到: verification_report.txt")
