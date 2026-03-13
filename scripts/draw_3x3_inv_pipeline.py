#!/usr/bin/env python3
"""
Draw the 3x3 symmetric matrix inversion hardware pipeline diagram.
Chinese font: Songti SC (宋体), English/math font: Times New Roman.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# ── Font config ────────────────────────────────────────────────────────────────
CN = 'Songti SC'
EN = 'Times New Roman'

fig, ax = plt.subplots(figsize=(18, 9))
ax.set_xlim(0, 18)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('white')

# ── Color palette ──────────────────────────────────────────────────────────────
STAGE_BG   = '#E8F4FD'
STAGE_EDGE = '#2E86C1'
BLOCK_BG   = '#FDFEFE'
BLOCK_EDGE = '#2874A6'
FIFO_BG    = '#EAF2FF'
RED        = '#C0392B'
ORANGE     = '#E67E22'
GREEN      = '#1E8449'
DARK       = '#1C2833'
GRAY       = '#717D7E'

# ── Helper functions ───────────────────────────────────────────────────────────
def box(ax, x, y, w, h, label, sublabel=None,
        fc=BLOCK_BG, ec=BLOCK_EDGE, fs=8, lw=1.2,
        bold=False, color=DARK, radius=0.15):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={radius}",
                          fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2 + (0.12 if sublabel else 0), label,
            ha='center', va='center', fontsize=fs,
            fontfamily=EN, fontweight=weight, color=color, zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.18, sublabel,
                ha='center', va='center', fontsize=fs-1,
                fontfamily=EN, color=RED, fontweight='bold', zorder=4)

def cn_label(ax, x, y, txt, fs=8.5, color=DARK, ha='center', va='center', bold=False):
    ax.text(x, y, txt, ha=ha, va=va, fontsize=fs,
            fontfamily=CN, color=color,
            fontweight='bold' if bold else 'normal', zorder=4)

def arrow(ax, x1, y1, x2, y2, color=DARK, lw=1.2, hw=0.12, hl=0.18):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=f'->', color=color, lw=lw,
                                mutation_scale=12),
                zorder=5)

def critical_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2.0,
                                mutation_scale=14),
                zorder=6)

# ── Stage background panels ────────────────────────────────────────────────────
stage_x = [0.2, 3.8, 7.0, 10.4, 14.2]
stage_w = [3.4, 3.0, 3.2, 3.6, 3.6]
stage_h = 8.4
for i, (sx, sw) in enumerate(zip(stage_x, stage_w)):
    rect = FancyBboxPatch((sx, 0.3), sw, stage_h,
                          boxstyle="round,pad=0,rounding_size=0.25",
                          fc=STAGE_BG, ec=STAGE_EDGE, lw=1.5, alpha=0.6, zorder=1)
    ax.add_patch(rect)

# Stage separators (dashed)
for sx in [3.7, 6.9, 10.3, 14.1]:
    ax.axvline(sx, ymin=0.035, ymax=0.965, color=STAGE_EDGE,
               lw=0.8, ls='--', alpha=0.5, zorder=2)

# ── Stage titles ───────────────────────────────────────────────────────────────
titles_cn = ['阶段一', '阶段二', '阶段三', '阶段四', '阶段五']
titles_en = ['元素寄存与时分调度', '双路并行乘法与差分', '行列式流水累加',
             '奇异性保护与归一化', '移位重排输出']
for i, (tx, tw, tcn, ten) in enumerate(zip(stage_x, stage_w,
                                            titles_cn, titles_en)):
    cx = tx + tw / 2
    cn_label(ax, cx, 8.45, tcn, fs=9.5, color=STAGE_EDGE, bold=True)
    ax.text(cx, 8.1, ten, ha='center', va='center', fontsize=7.5,
            fontfamily=CN, color=STAGE_EDGE, zorder=4)

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 – Input registers & mat_mux scheduling
# ══════════════════════════════════════════════════════════════════════════════
S1x = 0.2

# Input label
cn_label(ax, 0.35, 7.55, 'H_mm 输入', fs=7.5, ha='left')
ax.text(0.35, 7.25, '(6 elements × 64 bit)', ha='left', va='center',
        fontsize=6.5, fontfamily=EN, color=GRAY, zorder=4)
arrow(ax, 0.35, 7.0, 0.35, 6.6)

# Register bank
regs = ['h11', 'h12', 'h13', 'h22', 'h23', 'h33']
for i, r in enumerate(regs):
    rx = S1x + 0.22 + i * 0.52
    rect = FancyBboxPatch((rx, 6.0), 0.46, 0.52,
                          boxstyle="round,pad=0,rounding_size=0.06",
                          fc='#D6EAF8', ec=BLOCK_EDGE, lw=1.0, zorder=3)
    ax.add_patch(rect)
    ax.text(rx + 0.23, 6.26, r, ha='center', va='center',
            fontsize=7.5, fontfamily=EN, color=DARK, zorder=4)
ax.text(0.35, 5.85, '寄存器组', ha='left', va='center',
        fontsize=7, fontfamily=CN, color=GRAY, zorder=4)

# mat_mux circular shift register
mux_cx, mux_cy = 1.92, 5.0
mux_rect = FancyBboxPatch((mux_cx - 0.85, mux_cy - 0.35), 1.7, 0.7,
                           boxstyle="round,pad=0,rounding_size=0.1",
                           fc='#D5F5E3', ec='#1E8449', lw=1.2, zorder=3)
ax.add_patch(mux_rect)
ax.text(mux_cx, mux_cy + 0.08, 'mat_mux [5:0]', ha='center', va='center',
        fontsize=7.5, fontfamily=EN, color='#1E8449', fontweight='bold', zorder=4)
ax.text(mux_cx, mux_cy - 0.16, '循环移位寄存器', ha='center', va='center',
        fontsize=6.5, fontfamily=CN, color='#1E8449', zorder=4)
# Feedback arrow (curved)
ax.annotate('', xy=(mux_cx - 0.85, mux_cy + 0.1),
            xytext=(mux_cx + 0.85, mux_cy + 0.1),
            arrowprops=dict(arrowstyle='->', color='#1E8449', lw=1.2,
                            connectionstyle='arc3,rad=-0.45',
                            mutation_scale=10),
            zorder=5)
ax.text(mux_cx, mux_cy + 0.72, 'rotate each cycle', ha='center', va='center',
        fontsize=6.5, fontfamily=EN, color='#1E8449', zorder=4)

arrow(ax, 1.92, 6.0, 1.92, 5.37)
arrow(ax, 1.92, 4.63, 1.92, 4.05)

# MUX-A and MUX-B
box(ax, S1x + 0.32, 3.35, 1.4, 0.58, 'MUX-A',
    sublabel='→ (ax0, bx0)', fs=8, fc='#EBF5FB', ec=BLOCK_EDGE)
box(ax, S1x + 0.32, 2.6, 1.4, 0.58, 'MUX-B',
    sublabel='→ (ax1, bx1)', fs=8, fc='#EBF5FB', ec=BLOCK_EDGE)

# Cofactor schedule table
table_x, table_y = S1x + 0.18, 0.55
ax.text(table_x, table_y + 1.62, '周期', ha='center', va='center',
        fontsize=6.5, fontfamily=CN, color=DARK, fontweight='bold', zorder=4)
ax.text(table_x + 0.62, table_y + 1.62, '余子式', ha='center', va='center',
        fontsize=6.5, fontfamily=CN, color=DARK, fontweight='bold', zorder=4)
items = [('0','C11'),('1','C12'),('2','C13'),('3','C22'),('4','C23'),('5','C33')]
for k, (cyc, cof) in enumerate(items):
    yy = table_y + 1.28 - k * 0.22
    ax.text(table_x, yy, cyc, ha='center', va='center',
            fontsize=6.5, fontfamily=EN, color=DARK, zorder=4)
    ax.text(table_x + 0.62, yy, cof, ha='center', va='center',
            fontsize=7, fontfamily=EN, color=BLOCK_EDGE, fontweight='bold', zorder=4)

# Arrow from MUX to stage boundary
critical_arrow(ax, 3.05, 3.65, 3.75, 3.65)
critical_arrow(ax, 3.05, 2.9, 3.75, 3.35)

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 – Dual multipliers + subtractor + FIFO
# ══════════════════════════════════════════════════════════════════════════════
S2x = 3.85

# fp_m0
box(ax, S2x + 0.05, 4.5, 2.7, 0.75, 'fp_m0   ×',
    sublabel='Lat = 12 clk', fs=8.5, fc='#FDFEFE', ec=BLOCK_EDGE,
    bold=False)
# fp_m1
box(ax, S2x + 0.05, 3.45, 2.7, 0.75, 'fp_m1   ×',
    sublabel='Lat = 12 clk', fs=8.5, fc='#FDFEFE', ec=BLOCK_EDGE)

# Input labels
ax.text(S2x + 0.25, 5.0, '(ax0, bx0)', ha='left', va='center',
        fontsize=7, fontfamily=EN, color=GRAY, zorder=4)
ax.text(S2x + 0.25, 3.95, '(ax1, bx1)', ha='left', va='center',
        fontsize=7, fontfamily=EN, color=GRAY, zorder=4)

# Merge arrows to subtractor
arrow(ax, S2x + 2.75, 4.875, S2x + 2.75, 3.2)  # vertical merge

# fp_a0 subtractor
box(ax, S2x + 0.55, 2.5, 1.85, 0.65, 'fp_a0   −',
    sublabel='Lat = 14 clk', fs=8.5, fc='#FDFEFE', ec=BLOCK_EDGE)

# Arrow to FIFO
arrow(ax, S2x + 1.47, 2.5, S2x + 1.47, 1.65)

# FIFO
box(ax, S2x + 0.25, 0.85, 2.3, 0.75, 'FIFO',
    sublabel='depth = 32, 6 cofactors', fs=8.5,
    fc=FIFO_BG, ec='#2874A6', bold=True)

# Critical path arrow out
critical_arrow(ax, S2x + 2.75, 3.2, S2x + 2.75, 2.825)
critical_arrow(ax, 6.95, 2.825, 7.05, 2.825)

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 – Determinant accumulation
# ══════════════════════════════════════════════════════════════════════════════
S3x = 7.05

# Second multiplier
box(ax, S3x + 0.1, 4.4, 2.7, 0.75, 'FP MUL2   ×',
    sublabel='det term x (h11/h12/h13)', fs=8, fc='#FDFEFE', ec=BLOCK_EDGE)
arrow(ax, S3x + 1.45, 3.15, S3x + 1.45, 4.4)  # from stage2

# Sign-flip annotation
box(ax, S3x + 0.55, 3.6, 1.8, 0.55, '~sign bit flip~',
    fs=7.5, fc='#FDEDEC', ec='#C0392B', color=RED)
ax.text(S3x + 1.45, 3.4, '(cycle 1: C12 term)', ha='center', va='center',
        fontsize=6.5, fontfamily=EN, color=RED, zorder=4)

# Adder stage 1
box(ax, S3x + 0.35, 2.5, 2.1, 0.62, '第一级加法', fs=8,
    fc='#FDFEFE', ec=BLOCK_EDGE)
arrow(ax, S3x + 1.45, 5.15, S3x + 1.45, 5.65)
arrow(ax, S3x + 1.45, 3.6, S3x + 1.45, 3.12)
arrow(ax, S3x + 1.45, 3.12, S3x + 1.45, 2.5)  # approximate

# Adder stage 2
box(ax, S3x + 0.35, 1.6, 2.1, 0.62, '第二级加法', fs=8,
    fc='#FDFEFE', ec=BLOCK_EDGE)
arrow(ax, S3x + 1.45, 2.5, S3x + 1.45, 2.22)

# det output
ax.text(S3x + 1.45, 1.25, 'det(H_mm)', ha='center', va='center',
        fontsize=8.5, fontfamily=EN, color=GREEN, fontweight='bold', zorder=4)
arrow(ax, S3x + 1.45, 1.6, S3x + 1.45, 1.38)
critical_arrow(ax, S3x + 2.45, 1.91, 10.35, 1.91)

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 4 – Singularity guard + normalization
# ══════════════════════════════════════════════════════════════════════════════
S4x = 10.45

# FIFO read arrow from stage 2
arrow(ax, 6.22, 1.22, 10.45 + 0.1, 1.22)
ax.text(8.2, 1.05, '← 读取 6 个余子式', ha='center', va='center',
        fontsize=6.5, fontfamily=CN, color=GRAY, zorder=4)

# Comparator diamond
diamond_cx, diamond_cy = S4x + 1.7, 5.0
diamond_pts = np.array([
    [diamond_cx,        diamond_cy + 0.7],
    [diamond_cx + 1.1,  diamond_cy],
    [diamond_cx,        diamond_cy - 0.7],
    [diamond_cx - 1.1,  diamond_cy],
])
diamond = plt.Polygon(diamond_pts, fc='#FEF9E7', ec='#D4AC0D', lw=1.5, zorder=3)
ax.add_patch(diamond)
ax.text(diamond_cx, diamond_cy + 0.12, 'FP CMP', ha='center', va='center',
        fontsize=7.5, fontfamily=EN, fontweight='bold', color=DARK, zorder=4)
ax.text(diamond_cx, diamond_cy - 0.18, '|det| < 1e-12?', ha='center', va='center',
        fontsize=7, fontfamily=EN, color=RED, zorder=4)
arrow(ax, S4x + 1.7, 1.91, S4x + 1.7, 4.3)

# YES branch → zero output
ax.annotate('', xy=(S4x + 1.7, 4.0), xytext=(S4x + 1.7, 4.0),
            zorder=5)
arrow(ax, diamond_cx - 1.1, diamond_cy, diamond_cx - 1.8, diamond_cy)
ax.text(diamond_cx - 2.0, diamond_cy, '0', ha='center', va='center',
        fontsize=11, fontfamily=EN, color=RED, fontweight='bold', zorder=4)
ax.text(diamond_cx - 1.45, diamond_cy + 0.18, 'YES', ha='center', va='center',
        fontsize=6.5, fontfamily=EN, color=RED, zorder=4)

# NO branch → down
arrow(ax, diamond_cx, diamond_cy - 0.7, diamond_cx, diamond_cy - 1.5)
ax.text(diamond_cx + 0.2, diamond_cy - 0.9, 'NO', ha='left', va='center',
        fontsize=6.5, fontfamily=EN, color=GREEN, zorder=4)

# fp_d0 divider
box(ax, S4x + 0.4, 2.6, 2.55, 0.75, 'fp_d0   ÷',
    sublabel='Lat = 57 clk', fs=8.5, bold=False,
    fc='#FDFEFE', ec=BLOCK_EDGE)
# Lat annotation in red
ax.text(S4x + 1.7, 2.82, 'fp_d0   ÷', ha='center', va='center',
        fontsize=8.5, fontfamily=EN, color=DARK, fontweight='bold', zorder=5)
ax.text(S4x + 1.7, 2.62, 'Lat = 57 clk', ha='center', va='center',
        fontsize=8, fontfamily=EN, color=RED, fontweight='bold', zorder=5)

# mux_div
box(ax, S4x + 0.7, 1.5, 1.95, 0.62, 'mux_div',
    sublabel='det_small → 0', fs=7.5, fc='#EBF5FB', ec=BLOCK_EDGE)

arrow(ax, S4x + 1.7, 3.35, S4x + 1.7, 3.2)
arrow(ax, S4x + 1.7, 2.6, S4x + 1.7, 2.12)
critical_arrow(ax, S4x + 3.0, 2.975, 14.2, 2.975)

# ══════════════════════════════════════════════════════════════════════════════
# STAGE 5 – Shift register reorder & output
# ══════════════════════════════════════════════════════════════════════════════
S5x = 14.25

# Shift register chain
sr_labels = ['d0', 'd1', 'd2', 'd3', 'd4']
for i, lbl in enumerate(sr_labels):
    bx = S5x + 0.12 + i * 0.64
    by = 5.3
    rect = FancyBboxPatch((bx, by), 0.56, 0.58,
                          boxstyle="round,pad=0,rounding_size=0.07",
                          fc='#D6EAF8', ec=BLOCK_EDGE, lw=1.1, zorder=3)
    ax.add_patch(rect)
    ax.text(bx + 0.28, by + 0.34, lbl, ha='center', va='center',
            fontsize=8, fontfamily=EN, color=DARK, fontweight='bold', zorder=4)
    # Clock triangle
    ax.plot([bx + 0.18, bx + 0.28, bx + 0.38],
            [by - 0.1, by + 0.08, by - 0.1],
            color=GRAY, lw=0.8, zorder=4)
    # Chain arrows
    if i < 4:
        ax.annotate('', xy=(bx + 0.64, by + 0.29),
                    xytext=(bx + 0.56, by + 0.29),
                    arrowprops=dict(arrowstyle='->', color=DARK, lw=0.9,
                                    mutation_scale=8), zorder=5)

ax.text(S5x + 1.72, 6.18, '← 除法结果依次流入', ha='center', va='center',
        fontsize=6.5, fontfamily=CN, color=GRAY, zorder=4)
arrow(ax, 14.2, 2.975, S5x + 1.72, 5.3)

# res_cnt counter
box(ax, S5x + 0.52, 4.25, 2.25, 0.62, 'res_cnt [3:0]',
    sublabel='count 0 → 8', fs=7.5, fc='#FDFEFE', ec=BLOCK_EDGE)

# Output MUX
box(ax, S5x + 0.65, 3.0, 2.0, 0.88, 'Output MUX',
    sublabel='9 taps select', fs=8, fc='#EBF5FB', ec=BLOCK_EDGE, bold=True)
arrow(ax, S5x + 1.65, 5.3, S5x + 1.65, 4.87)
arrow(ax, S5x + 1.65, 4.25, S5x + 1.65, 3.88)

# Reuse annotation
ann_items = [
    ('cnt 3 -> d2: m21=m12',),
    ('cnt 6 -> d4: m31=m13',),
    ('cnt 7 -> d3: m32=m23',),
]
for k, (txt,) in enumerate(ann_items):
    ax.text(S5x + 0.18, 2.6 - k * 0.28, txt, ha='left', va='center',
            fontsize=6, fontfamily=EN, color=ORANGE, zorder=4)
ax.text(S5x + 0.18, 2.7, '对称复用:', ha='left', va='center',
        fontsize=6.5, fontfamily=CN, color=ORANGE, fontweight='bold', zorder=4)

# Final output
box(ax, S5x + 0.3, 1.3, 2.9, 0.72, 'Hmm_inv  (9 elements, serial)',
    fs=8, fc='#D5F5E3', ec=GREEN, bold=True, color=GREEN)
arrow(ax, S5x + 1.65, 3.0, S5x + 1.65, 2.02)

# ── Legend ─────────────────────────────────────────────────────────────────────
legend_patches = [
    mpatches.Patch(fc='white', ec=ORANGE, lw=2, label='Critical data path (关键路径)'),
    mpatches.Patch(fc='white', ec=RED,   lw=2, label='Latency (流水延迟, 拍数)'),
    mpatches.Patch(fc='#D5F5E3', ec=GREEN, lw=1.5, label='Final output'),
]
ax.legend(handles=legend_patches, loc='lower left',
          fontsize=7, framealpha=0.85,
          prop={'family': EN, 'size': 7},
          bbox_to_anchor=(0.0, 0.0))

# ── Figure caption ─────────────────────────────────────────────────────────────
ax.text(9, 0.12,
        '图 4-X   3×3 对称矩阵求逆模块硬件流水线结构',
        ha='center', va='center', fontsize=10,
        fontfamily=CN, color=DARK, fontweight='bold', zorder=4)

plt.tight_layout(pad=0.3)
plt.savefig('/Users/byheng/Dissertation/Img/3x3_inv_pipeline.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Saved: Img/3x3_inv_pipeline.png")
